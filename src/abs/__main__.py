import typer

from abs.util import add_command

from abs import ascceg

app = typer.Typer()

@app.callback()
def callback():
    """Fetch *tidy* data from ABS

    Specify the desired datasource with subcommands.
    """

# Add ABS subcommands here.
# The module MUST define a function `df` which returns a Polars
# DataFrame containing the required data.
# The command name will be automatically derived from the module name.
# The command help text will be automatically derived from the module
# docstring.
add_command(app, ascceg)

if __name__ == "__main__":
    app()
