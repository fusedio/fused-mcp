# Fused MCP: Setting up MCP Servers for Data Scientists

This repo offers a simple step-by-step notebook workflow to setup MCP Servers with Claude's Desktop App, all in Python built on top of Fused User Defined Functions (UDFs).

<!-- TODO: Add GIF of installed setup so people can see what this looks like -->

## Requirements
- Python 3.13
- [Claude Desktop app](https://claude.ai/download) installed
<!-- - `uv` installed  -->


## Installation

- Clone this repo in any local directory:

```bash
git clone https://github.com/fusedio/udf-test.git
```


[Optionally]  Install `uv` if you don't have it:

Macos / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

[Optionally #2] Activate your virtual environment

```bash
uv venv
```

- Install dependencies directly:

```bash
pip install fused "fused[all]>=1.14.2" "jupyterlab>=4.3.6" "mcp[cli]>=1.4.1"
```

- Test out the client by asking for its info:

```bash
python run.py -h
```

- Open the `setting_up_udf_mcp.ipynb` notebook in your favorite local IDE & follow instructions from there

<!-- TODO: Need to add steps to run notebook-->

## Repository structure

This repo is build on top of [MCP Server](https://modelcontextprotocol.io/introduction) & [Fused UDFs](https://docs.fused.io/core-concepts/write/) which are Python functions that can be run from anywhere.

<!-- TODO: Explain a bit of how repo works & abstracts away some of the MCP server setup -->

## Support & Community

Feel free to join our [Discord server](https://discord.com/invite/BxS5wMzdRk) if you want some help getting unblocked!