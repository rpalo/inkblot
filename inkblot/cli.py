"""The CLI Interface for inkblot."""

import argparse
import pathlib

from livereload import Server, shell

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
    watch_dir = project_dir / user_config["source_dir"]

    server = Server()
    server.watch(watch_dir, shell(f"inkblot build {project_dir}"))
    server.serve(root=serve_dir, port=args.port, open_url_delay=0.5)
    


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