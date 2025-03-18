import asyncio
import json
import os
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client

from anthropic import Anthropic
from dotenv import load_dotenv

# NOTE this needs a ANTHROPIC_API_KEY in .env to work
load_dotenv()  # load environment variables from .env
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"

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
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{ 
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        print(f"Available tools: {[t['name'] for t in available_tools]}")
        print(f"Available tools description: {[t['description'] for t in available_tools]}")
        print(f"Available input_schema: {[t['input_schema'] for t in available_tools]}")

        # Initial Claude API call
        print("Sending query to Claude...")
        response = self.anthropic.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        # Process response and handle tool calls
        tool_results = []
        final_text = []

        assistant_message_content = []
        for content in response.content:
            if content.type == 'text':
                print("Received text response from Claude")
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input
                
                print(f"Claude is calling tool: {tool_name} with args: {tool_args}")
                
                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # Continue conversation with tool results
                assistant_message_content.append(content)
                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content
                        }
                    ]
                })

                # Get next response from Claude
                print("Sending tool results to Claude for follow-up...")
                response = self.anthropic.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=1000,
                    messages=messages,
                    tools=available_tools
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)
    
    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
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
        print("Example: python clientsse.py https://dev.udf.ai/chat/4a693c58-dbd3-4f08-a07e-2ec305a8bf29/sse")
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