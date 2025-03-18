import fused
import argparse


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run an MCP server with UDF tools")
    parser.add_argument(
        "--tokens",
        required=False,
        help="Comma-separated list of token IDs to register as tools",
    )
    parser.add_argument(
        "--runtime",
        default="remote",
        required=False,
        help="Runtime to use (local, remote)",
    )
    parser.add_argument(
        "--udf-names",
        help="Comma-separated list of UDF (folder) names to register as tools",
    )
    parser.add_argument("--name", default="udf-server", help="Server name")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    args = parser.parse_args()

    # Process token and udf_names arguments
    tokens = args.tokens.split(",") if args.tokens else None
    udf_names = args.udf_names.split(",") if args.udf_names else None

    commit = "699ad0e"
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
