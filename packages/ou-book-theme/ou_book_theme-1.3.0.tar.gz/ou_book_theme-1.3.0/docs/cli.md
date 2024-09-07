# Command-line

The OU Book Theme provides an extension to the JupyterBook Command-line (CLI). To run
the CLI commands use:

:::{code-block} shell
$ jupyter-book obt {COMMAND}
:::

The following additional CLI commands are available:

## serve - Run a local development server

Use the `serve` command to run a local development server:

:::{code-block} shell
$ jupyter-book obt serve {PATH}
:::

The JupyterBook is then available at http://localhost:8000.

When you make changes to the book content, the book is automatically rebuilt and the web-page reloaded.
Depending on the size of the book, this may take a few seconds. Check the terminal for any errors.

You can configure the host and port to make the book available at by providing the `--host {IP_OR_HOSTNAME}`
and / or `--port {PORT}` options to the `serve` command.
