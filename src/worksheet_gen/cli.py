from __future__ import annotations

import argparse
from pathlib import Path

from .load import load_yaml
from .render import render_pdf


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="worksheet-gen")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render", help="Render a worksheet PDF")
    render_parser.add_argument("input", help="Input YAML path")
    render_parser.add_argument("output", help="Output PDF path")

    serve_parser = subparsers.add_parser("serve", help="Run the web preview server")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    serve_parser.add_argument("--port", default=8000, type=int, help="Bind port")

    args = parser.parse_args(argv)

    if args.command == "render":
        input_path = Path(args.input)
        output_path = Path(args.output)
        worksheet = load_yaml(input_path)
        render_pdf(worksheet, output_path, base_dir=input_path.resolve().parent)
    elif args.command == "serve":
        from .web import app
        import uvicorn

        uvicorn.run(app, host=args.host, port=args.port)
