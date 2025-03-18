# Fused MCP: Setting up MCP Servers for Data Scientists

This repo offers a simple step-by-step notebook workflow to setup MCP Servers with Claude's Desktop App, all in Python built on top of Fused User Defined Functions (UDFs).

<!-- TODO: Add GIF of installed setup so people can see what this looks like -->

## Requirements
- Python 3.13
- [Claude Desktop app](https://claude.ai/download) installed
- `uv` installed 


## Installation

- Clone this repo in any local directory:

```bash
git clone git@github.com:fusedio/udf-test.git
```

- Install `uv` if you don't have it:

    Macos:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Windows:
    ```
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

- Navigate to the repo & install it:

```bash
cd udf-test/
uv run run.py --info
```

- Open the `setting_up_udf_mcp.ipynb` notebook in your favorite local IDE & follow instructions from there

<!-- TODO: Need to add steps to run notebook-->

## Repository structure

This repo is build on top of [MCP Server](https://modelcontextprotocol.io/introduction) & [Fused UDFs](https://docs.fused.io/core-concepts/write/) which are Python functions that can be run from anywhere.

<!-- TODO: Explain a bit of how repo works & abstracts away some of the MCP server setup -->