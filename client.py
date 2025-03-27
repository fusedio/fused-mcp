import asyncio
import json
import os
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self._session_context = None
        self._streams_context = None
        self.anthropic = Anthropic()

    async def connect_to_sse_server(self, server_url: str):
        """
        Connect to an MCP server running with SSE transport

        Args:
            server_url: The URL of the SSE endpoint
        """
        print(f"Connecting to SSE endpoint: {server_url}")

        try:
            # Create the SSE client
            self._streams_context = sse_client(url=server_url)
            streams = await self._streams_context.__aenter__()

            self._session_context = ClientSession(*streams)
            self.session = await self._session_context.__aenter__()

            # Initialize
            print("Initializing SSE client...")
            await self.session.initialize()

            # List available tools to verify connection
            print("Connection established, listing tools...")
            response = await self.session.list_tools()
            tools = response.tools
            print("\nConnected to server with tools:", [tool.name for tool in tools])
            return True
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            await self.cleanup()
            return False

    async def cleanup(self):
        """Properly clean up the session and streams"""
        try:
            if self._session_context:
                await self._session_context.__aexit__(None, None, None)
            if self._streams_context:
                await self._streams_context.__aexit__(None, None, None)
            print("Cleaned up connection resources")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

        print(f"Available tools: {[t['name'] for t in available_tools]}")

        # Initial Claude API call
        print("Sending query to Claude...")
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
        )

        # Track complete conversation
        final_text = []
        
        # Continue conversation until no more tool calls
        while True:
            # Process the most recent response
            contains_tool_calls = False
            assistant_message_content = []
            
            # First, collect all tool calls without executing them
            pending_tool_calls = []
            
            # Process all content blocks from this response
            for content in response.content:
                if content.type == "text":
                    print("Received text response from Claude")
                    final_text.append(content.text)
                    assistant_message_content.append(content)
                elif content.type == "tool_use":
                    contains_tool_calls = True
                    # Store the tool call info for parallel execution
                    pending_tool_calls.append({
                        "tool_name": content.name,
                        "tool_args": content.input,
                        "tool_id": content.id
                    })
                    
                    final_text.append(f"[Queueing tool call: {content.name} with args {content.input}]")
                    assistant_message_content.append(content)
            
            # If no tool calls, we're done
            if not contains_tool_calls:
                break
                
            # Execute all tool calls in parallel
            print(f"Executing {len(pending_tool_calls)} tool calls in parallel...")
            tool_tasks = [
                self.session.call_tool(call["tool_name"], call["tool_args"]) 
                for call in pending_tool_calls
            ]
            
            # Wait for all tool calls to complete
            tool_results = await asyncio.gather(*tool_tasks)
            
            # Process results and build the response message
            tool_result_content = []
            for i, result in enumerate(tool_results):
                tool_call = pending_tool_calls[i]
                tool_result_content.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call["tool_id"],
                    "content": result.content
                })
                
                # Add to final text for display
                final_text.append(
                    f"[Tool result for {tool_call['tool_name']}: {result.content}]"
                )
            
            # Append assistant message with all tool calls
            messages.append({
                "role": "assistant",
                "content": assistant_message_content
            })
            
            # Add a single user message with all tool results
            messages.append({
                "role": "user",
                "content": tool_result_content
            })
            
            # Get next response from Claude with all tool results
            print(f"Sending {len(tool_results)} tool results to Claude for follow-up...")
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=messages,
                tools=available_tools,
            )
        
        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                print("Processing query...")
                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")
                import traceback

                traceback.print_exc()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python clientsse.py <URL of SSE MCP server>")
        print(
            "Example: python clientsse.py https://dev.udf.ai/chat/4a693c58-dbd3-4f08-a07e-2ec305a8bf29/sse"
        )
        sys.exit(1)

    server_url = sys.argv[1]
    client = MCPClient()
    try:
        success = await client.connect_to_sse_server(server_url=server_url)
        if success:
            await client.chat_loop()
        else:
            print("Failed to connect. Exiting.")
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        print("Cleaning up client...")
        await client.cleanup()


if __name__ == "__main__":
    import sys

    asyncio.run(main())