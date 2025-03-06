from pathlib import Path
from typing import Annotated

import polars as pl
import polars.selectors as cs
from polars import col
import typer

# Remove fallback to backports.strenum once we drop support for Python
# 3.10 (no sooner than 2026-10).
try:
    from enum import StrEnum
except ImportError:
    from backports.strenum import StrEnum

app = typer.Typer()


def df():
    """Fetch Australian Standard Classification of Cultural and Ethnic
    Groups (ASCCEG) data from ABS.

    Return a tidy Polars DataFrame
    """
    ascceg_file = "https://www.abs.gov.au/statistics/classifications/australian-standard-classification-cultural-and-ethnic-groups-ascceg/2019/12490do0001_201912.xls"

    digits = r"^\d+$"

    # Load both sheets at once to avoid downloading the file twice
    dfs = pl.read_excel(
        ascceg_file,
        sheet_name=["Table 1.3", "Table 2"],
        has_header=False,
    )

    main_groups = (
        dfs["Table 1.3"]
        .with_row_index()
        .filter(col("index") >= 9)
        .select(col("column_3").alias("code"), col("column_4").alias("group"))
        .filter(col("code").str.contains(digits))
    )

    supplementary_groups = (
        dfs["Table 2"]
        .with_row_index()
        .filter(col("index") >= 4)
        .select(col("column_1").alias("code"), col("column_2").alias("group"))
        .filter(col("code").str.contains(digits))
        .with_columns(col("code").str.pad_start(4, "0"))
    )

    all_groups = pl.concat([main_groups, supplementary_groups]).sort("code")

    return all_groups


class SupportedFiletype(StrEnum):
    parquet = "parquet"
    csv = "csv"


@app.command()
def ascceg(
    output: Annotated[
        Path,
        typer.Argument(
            help="directory or filepath to save output file",
            show_default="ascceg.parquet",
        ),
    ] = Path(),
    filetype: Annotated[
        SupportedFiletype | None,
        typer.Option(
            "--filetype",
            "-f",
            help="filetype (not required if specified in file suffix)",
            show_default=SupportedFiletype.parquet,
        ),
    ] = None,
):
    """Fetch Australian Standard Classification of Cultural and Ethnic
    Groups (ASCCEG) data from ABS as Parquet or CSV.
    """

    default_filetype = "parquet"

    # Abort if conflict between specified filetype and file suffix
    if filetype and filetype != output.suffix and not output.is_dir():
        print(
            f"Error: File suffix '{output.suffix}' does not match specified "
            f"filetype '{filetype}'"
        )
        print("Hint: --filetype is not required if already specified in the filename")
        raise typer.Abort()

    ascceg_df = df()

    if output.is_dir():
        output = output / f"ascceg.{filetype or default_filetype}"

    if output.suffix == ".parquet":
        ascceg_df.write_parquet(output)
    elif output.suffix == ".csv":
        ascceg_df.write_csv(output)
