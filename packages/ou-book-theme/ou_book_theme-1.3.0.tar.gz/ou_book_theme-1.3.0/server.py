"""Temporary dev server."""

from livereload import Server, shell

path = "docs"
port = 8000
host = "0.0.0.0"  # noqa: S104

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
