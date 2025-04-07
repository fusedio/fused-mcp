<h1 align="center">
   Fused MCP Agents: Setting up MCP Servers for Data
</h1>

<p align="center">
<a href="/LICENSE" target="_blank"><img src='https://img.shields.io/badge/license-MIT-green?style=for-the-badge' /></a>&nbsp;<img src='https://img.shields.io/badge/Agents-3-green?style=for-the-badge' />&nbsp;<a href='https://discord.com/invite/Eryz9P2DeY'><img src='https://img.shields.io/badge/Fused-udf-d1e550?style=for-the-badge' /></a>
</p>

<p align="center">
  <a
    href="https://docs.fused.io/"
    target="_blank"
  ><b>Documentation</b></a>&nbsp;&nbsp;&nbsp;🌪️&nbsp;&nbsp;&nbsp;
   <a
    href="https://docs.fused.io/blog/announcing-fused-ai-builder/"
    target="_blank"
  ><b>Read the announcement</b>
 </a>&nbsp;&nbsp;&nbsp;🔥&nbsp;&nbsp;&nbsp;
  <a
    href="https://discord.com/invite/Eryz9P2DeY"
    target="_blank"
  >
    <b>Join Discord</b>
  </a>
</p>


[MCP servers](https://modelcontextprotocol.io/introduction) allow LLMs like Claude to make HTTP requests, connecting them to APIs & executable code. We built this repo for ourselves & anyone working with data to easily pass _any_ Python code directly to your own desktop Claude app. 


<h1 align="center">
  <a
    target="_blank"
    href="https://fused.io"
  >
    <img
      align="center"
      alt="UDF AI"
src="https://raw.githubusercontent.com/fusedio/fused-docs/refs/heads/main/blog/2025-04-01-announcing-ai-builder/Fused_AI_Builder_graph.png"
      style="width:100%;"
    />
    
  </a>
</h1>



This repo offers a simple step-by-step notebook workflow to setup [MCP Servers](https://modelcontextprotocol.io/introduction) with Claude's Desktop App, all in Python built on top of Fused [User Defined Functions](https://docs.fused.io/core-concepts/write/) (UDFs).

![Demo once setup](https://fused-magic.s3.us-west-2.amazonaws.com/udf-mcp-repo/readme_asset/mcp_demo_fused_notebook_2.5x.gif)

## Requirements
- Python 3.11
- Latest [Claude Desktop app](https://claude.ai/download) installed (macOS & Windows)

If you're on Linux, the desktop app isn't available so [we've made a simple client](#using-a-local-claude-client-without-claude-desktop-app) you can use to have it running locally too!

You do _not_ need a Fused account to do any of this! All of this will be running on your local machine.

## Installation

- Clone this repo in any local directory, and navigate to the repo: 

  ```bash
  git clone https://github.com/fusedio/fused-mcp.git
  cd fused-mcp/
  ```

- Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
  if you don't have it:

  macOS / Linux:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

  Windows:
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- Test out the client by asking for its info:

  ```bash
  uv run main.py -h
  ```

- Start by following our getting-started notebook [`fused_mcp_agents.ipynb`](1.fused_mcp_agents.ipynb) in your favorite local IDE to get set up and then make your way to the more advanced notebook to [make your own Agents & functions](2.create_your_own_agents.ipynb)

![Notebook](/img/Starting_notebook.gif)

## Repository structure

This repo is build on top of [MCP Server](https://modelcontextprotocol.io/introduction) & [Fused UDFs](https://docs.fused.io/core-concepts/write/) which are Python functions that can be run from anywhere.

## Support & Community

Feel free to join our [Discord server](https://discord.com/invite/BxS5wMzdRk) if you want some help getting unblocked!

Here are a few common steps to debug the setup:

-  Running `uv run main.py -h` should return something like this:

![uv helper output function](/img/uv_run_helper_output.png)

- You might need to pass global paths to some functions to the `Claude_Desktop_Config.json`. For example, by default we only pass `uv`:

```json
{
    "mcpServers": {
        "qgis": {
            "command": "uv",
            "args": ["..."]
        }

    }
}
```

But you might need to pass the full path to `uv`, which you can simply pass to `common.generate_local_mcp_config` in the notebook:

```python
# in fused_mcp_agents.ipynb
import shutil 

common.generate_local_mcp_config(
    config_path=PATH_TO_CLAUDE_CONFIG,
    agents_list = ["get_current_time"],
    repo_path= WORKING_DIR,
    uv_path=shutil.which('uv'),
)
```

Which would create a config like this:

```json
{
    "mcpServers": {
        "qgis": {
            "command": "/Users/<YOUR_USERNAME>/.local/bin/uv",
            "args": ["..."]
        }

    }
}
```

-  If Claude runs without showing any connected tools, take a look at the [MCP Docs for troubleshooting the Claude Desktop setup](https://modelcontextprotocol.io/quickstart/server#claude-for-desktop-integration-issues)

## Contribute

Feel free to open PRs to add your own UDFs to `udfs/` so others can play around with them locally too!

## Using a local Claude client (without Claude Desktop app)

If you are unable to install the Claude Desktop app (e.g., on Linux), we provide
a small example local client interface to use Claude with the MCP server configured
in this repo:

NOTE: You'll need an API key for Claude here as you won't use the Desktop App

- Create an [Anthropic Console Account](https://console.anthropic.com/)
- Create an [Anthropic API Key](https://console.anthropic.com/settings/keys)

- Create a `.env`:
  ```bash
  touch .env
  ```

- Add your  key as `ANTHROPIC_API_KEY` inside the `.env`:

  ```
  # .env
  ANTHROPIC_API_KEY = "your-key-here"
  ```

- Start the MCP server:

  ```bash
  uv run main.py --agent get_current_time
  ```

- In another terminal session, start the local client, pointing to the address of the server:

  ```bash
  uv run client.py http://localhost:8080/sse
  ```
