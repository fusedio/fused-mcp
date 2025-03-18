# Fused MCP: Setting up MCP Servers for Data Scientists

MCP servers allow Claude & other LLMs to make HTTP requests, connecting them to APIs & executable code. We built this repo for ourselves & other data scientists to easily pass _any_ Python code directly to your own desktop Claude app. 

This repo offers a simple step-by-step notebook workflow to setup [MCP Servers](https://modelcontextprotocol.io/introduction) with Claude's Desktop App, all in Python built on top of Fused [User Defined Functions](https://docs.fused.io/core-concepts/write/) (UDFs).

![Demo once setup](https://fused-magic.s3.us-west-2.amazonaws.com/udf-mcp-repo/readme_asset/mcp_demo_fused_notebook_2.5x.gif)

<!-- TODO: Add GIF of installed setup so people can see what this looks like -->

## Requirements
- Python 3.13
- Latest [Claude Desktop app](https://claude.ai/download) installed (note this is only available on MacOS & Windows for now)

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

- Open the `setting_up_udf_mcp.ipynb` notebook in your favorite local IDE & follow instructions from there.

<!-- TODO: Need to add steps to run notebook-->

## Repository structure

This repo is build on top of [MCP Server](https://modelcontextprotocol.io/introduction) & [Fused UDFs](https://docs.fused.io/core-concepts/write/) which are Python functions that can be run from anywhere.

<!-- TODO: Explain a bit of how repo works & abstracts away some of the MCP server setup -->

## Support & Community

Feel free to join our [Discord server](https://discord.com/invite/BxS5wMzdRk) if you want some help getting unblocked!

## Contribute

Feel free to open PRs to add your own UDFs to `udfs/` so others can play around with them locally to!