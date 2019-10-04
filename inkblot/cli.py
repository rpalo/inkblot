"""The CLI Interface for inkblot."""

import argparse
from functools import partial
import http.server
import pathlib
import socketserver

from inkblot import config
from inkblot.inkblot import generate

def build(args):
    project_dir = args.directory
    if (project_dir / "config.yaml").exists():
        user_config = config.config_from_file(project_dir / "config.yaml")
    else:
        user_config = config.DEFAULT_CONFIG

    generate(project_dir, config=user_config)


def serve(args):
    project_dir = args.directory
    if (project_dir / "config.yaml").exists():
        user_config = config.config_from_file(project_dir / "config.yaml")
    else:
        user_config = config.DEFAULT_CONFIG

    serve_dir = project_dir / user_config["build_dir"]

    Handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(serve_dir))
    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        print("Now serving at port", args.port)
        httpd.serve_forever()


def run():
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest="subcommand")

    build_parser = subcommands.add_parser("build", help="Compile the site.")
    build_parser.add_argument("-d", "--directory", default=".", type=pathlib.Path, help="the project directory")
    build_parser.set_defaults(func=build)

    serve_parser = subcommands.add_parser("serve", help="Serve the site on a local development server.")
    serve_parser.add_argument("-d", "--directory", default=".", type=pathlib.Path, help="the project directory")
    serve_parser.add_argument("-p", "--port", type=int, default=8000, help="localhost port from which to serve")
    serve_parser.set_defaults(func=serve)

    args = parser.parse_args()
    if args.subcommand:
        args.func(args)
    else:
        parser.print_help()