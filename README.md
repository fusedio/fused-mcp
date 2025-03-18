# Fused MCP Agents: Setting up MCP Servers for Data Scientists

MCP servers allow Claude & other LLMs to make HTTP requests, connecting them to APIs & executable code. We built this repo for ourselves & other data scientists to easily pass _any_ Python code directly to your own desktop Claude app. 

This repo offers a simple step-by-step notebook workflow to setup [MCP Servers](https://modelcontextprotocol.io/introduction) with Claude's Desktop App, all in Python built on top of Fused [User Defined Functions](https://docs.fused.io/core-concepts/write/) (UDFs).

![Demo once setup](https://fused-magic.s3.us-west-2.amazonaws.com/udf-mcp-repo/readme_asset/mcp_demo_fused_notebook_2.5x.gif)

## Requirements
- Python 3.11
- Latest [Claude Desktop app](https://claude.ai/download) installed (MacOS & Windows)

If you're on Linux, the desktop app isn't available so [we've made a simple client](#using-a-local-claude-client-without-claude-desktop-app) you can use to have it running locally too!

You do _not_ need a Fused account to do any of this! All of this will be running on your local machine

## Installation

- Clone this repo in any local directory, and navigate to the repo:

  ```bash
  git clone https://github.com/fusedio/udf-test.git
  cd udf-test/
  ```

- Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
  if you don't have it:

  Macos / Linux:
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

This should give you something like:

![uv helper output function](/img/uv_run_helper_output.png)

- Open the `fused_mcp_agents.ipynb` notebook in your favorite local IDE & follow instructions from there.

## Repository structure

This repo is build on top of [MCP Server](https://modelcontextprotocol.io/introduction) & [Fused UDFs](https://docs.fused.io/core-concepts/write/) which are Python functions that can be run from anywhere.

## Support & Community

Feel free to join our [Discord server](https://discord.com/invite/BxS5wMzdRk) if you want some help getting unblocked!

## Contribute

Feel free to open PRs to add your own UDFs to `udfs/` so others can play around with them locally to!

## Using a local Claude client (without Claude Desktop app)

If you are unable to install the Claude Desktop app (e.g., on Linux), we provide
a small example local client interface to use Claude with the MCP server configured
in this repo:

- This workflow requires an API key Claude as an environment variable. For example,
  add a `.env` file in this repo with an `ANTHROPIC_API_KEY` entry.

- Start the MCP server:

  ```bash
  uv run main.py --agent get_current_time
  ```

- In another terminal session, start the local client, pointing to the address of the server:

  ```bash
  uv run client.py http://localhost:8080/sse
  ```
