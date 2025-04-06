# Code duplicated from fused-mcp repo
import argparse
import json
import os

import fused
from loguru import logger


def disable_fused_auth():
    from fused._auth import AUTHORIZATION

    def _noop_initialize(*args, **kwargs):
        logger.debug("AUTHORIZATION.initialize intercepted")

    setattr(AUTHORIZATION, "initialize", _noop_initialize)


def main():
    # Do not import code from untrusted UDFs in this context
    fused.options.never_import = True
    disable_fused_auth()

    env_base_url = os.environ.get("FUSED_BASE_URL", None)
    if env_base_url:
        env_base_url += "/v1"
        logger.info(f"Using {env_base_url=}")
        fused.options.base_url = env_base_url
        os.environ["FUSED_NO_SET_ENV"] = "1"

    parser = argparse.ArgumentParser(description="Run an MCP server with UDF tools")
    parser.add_argument(
        "--tokens",
        required=False,
        default=os.environ.get("UDF_TOKENS", None),
        help="Comma-separated list of token IDs to register as tools",
    )
    parser.add_argument(
        "--udf-names",
        help="Comma-separated list of UDF (folder) names to register as tools",
    )
    parser.add_argument(
        "--agent",
        help="The agent name for which to register its UDFs as tools (as specified in agents.json)",
    )
    parser.add_argument(
        "--runtime",
        default="remote",
        required=False,
        help="Runtime to use (local, remote)",
    )

    parser.add_argument("--name", default="udf-server", help="Server name")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument(
        "--commit",
        type=str,
        # Defaulting to always main for udfs repo to use latest code for common-mcp
        default=os.environ.get("COMMIT", "main"),
        help="common-mcp commit used for run_server",
    )
    args = parser.parse_args()

    # Process token and udf_names arguments
    tokens = args.tokens.split(",") if args.tokens else None
    udf_names = args.udf_names.split(",") if args.udf_names else None
    agent = args.agent
    commit = args.commit

    if agent:
        if tokens is not None or udf_names is not None:
            raise ValueError("Cannot specify both agent and tokens or udf-names")
        with open("agents.json") as f:
            agents_list = json.load(f)["agents"]

        agents = [a for a in agents_list if a["name"] == agent]
        if not len(agents) == 1:
            raise ValueError(f"Agent '{agent}' not found in agents.json")

        udf_names = agents[0]["udfs"]

    logger.info(f"{tokens=}")
    logger.info(f"{udf_names=}")
    logger.info(f"{agent=}")
    logger.info(f"{commit=}")

    mcp_utils = fused.load(
        f"https://github.com/fusedio/udfs/tree/{commit}/public/common_mcp"
    ).utils

    # Call the run_server function with parsed arguments
    mcp_utils.run_server(
        server_name=args.name,
        runtime=args.runtime,
        host=args.host,
        port=args.port,
        tokens=tokens,
        udf_names=udf_names,
    )


if __name__ == "__main__":
    main()
