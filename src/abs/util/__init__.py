from collections.abc import Callable
from pathlib import Path
from typing import Annotated
from types import ModuleType

import polars as pl
import typer

# Remove fallback to backports.strenum once we drop support for Python
# 3.10 (no sooner than 2026-10).
from enum import auto

try:
    from enum import StrEnum
except ImportError:
    from backports.strenum import StrEnum


class SupportedFileType(StrEnum):
    PARQUET = auto()
    CSV = auto()


def add_command(
    app: typer.Typer,
    module: ModuleType,
    # name: str,
    # df_func: Callable[[], pl.DataFrame],
    # help: str = "",
) -> None:
    """Dynamically add a new CLI subcommand

    Arguments:
        app: A top-level Typer app.
        module: The module to wrap with a subcommand.
            The module MUST provide a function called 'df' which returns
            a Polars DataFrame.
        # name: The name of the new subcommand.
        # df_func: Function which returns the data required by the subcommand.
        # help: Help for the new subcommand.

    Returns:
        None
    """

    name = module.__name__.rsplit('.', maxsplit=1)[-1]
    df_func = module.df
    help = module.__doc__

    def command(
        output: Annotated[
            Path,
            typer.Argument(
                help="directory or filepath to save output file",
                show_default=f"{name}.parquet",
            ),
        ] = Path(),
        filetype: Annotated[
            SupportedFileType | None,
            typer.Option(
                "--filetype",
                "-f",
                help="filetype (not required if specified in file suffix)",
                show_default=SupportedFileType.PARQUET,
            ),
        ] = None,
    ):
        default_filetype = "parquet"

        # Abort if conflict between specified filetype and file suffix
        if filetype and filetype != output.suffix and not output.is_dir():
            print(
                f"Error: File suffix '{output.suffix}' does not match specified "
                f"filetype '{filetype}'"
            )
            print(
                "Hint: --filetype is not required if already specified in the filename"
            )
            raise typer.Abort()

        df = df_func()

        if output.is_dir():
            output = output / f"{name}.{filetype or default_filetype}"

        if output.suffix == ".parquet":
            df.write_parquet(output)
        elif output.suffix == ".csv":
            df.write_csv(output)

    # Dynamically add docstring
    command.__doc__ = help

    app.command(name=name)(command)
