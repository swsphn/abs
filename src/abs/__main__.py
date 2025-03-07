# NOTE: If you are trying to add a new data source and sub-command, you
# DO NOT need to edit this file.
#
# Simply add a top-level module with the same name as the datasource to
# the `src/abs` directory. Ensure it has a descriptive docstring, and
# a `df` function which returns the data as a Polars DataFrame. It will
# then be automatically imported, and added as a CLI sub-command.

import typer

import abs
from abs.util import add_command

app = typer.Typer()


@app.callback()
def callback():
    """Fetch *tidy* data from ABS

    Specify the desired datasource with subcommands.
    """


# This *automatically* adds abs subcommands.
# Modules providing data sources MUST be located at the top level under
# 'src/abs/<module>.py`.
# The module MUST define a function `df` which returns a Polars
# DataFrame containing the required data.
# The command name will be automatically derived from the module name.
# The command help text will be automatically derived from the module
# docstring.
for module_name in abs.__all__:
    module = getattr(abs, module_name)
    add_command(app, module)

if __name__ == "__main__":
    app()
