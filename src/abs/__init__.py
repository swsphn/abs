import typer

from .ascceg import app as ascceg_app

app = typer.Typer()

app.add_typer(ascceg_app)

if __name__ == "__main__":
    app()
