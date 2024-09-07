"""JupyterBook CLI extension."""

import click
from livereload import Server, shell


@click.group()
def main() -> None:
    """Command-line for the OU Book Theme."""
    pass


@click.command()
@click.argument("path")
@click.option("--host", default="127.0.0.1", help="The host to serve the book at")
@click.option("--port", default=8000, type=int, help="The port to serve the book at")
def serve(path: str, host: str, port: int) -> None:
    """Serve the JupyterBook locally."""
    partial_build = shell(f"jb build {path}")
    full_build = shell(f"jb build {path} --all")
    full_build()

    server = Server()
    server.watch(f"{path}/**/*.md", partial_build)
    server.watch(f"{path}/**/*.yml", full_build)
    server.watch(f"{path}/**/*.png", full_build)
    server.watch(f"{path}/**/*.jpg", full_build)
    server.watch(f"{path}/**/*.jpeg", full_build)
    server.serve(root=f"{path}/_build/html", port=port, host=host)


main.add_command(serve)
