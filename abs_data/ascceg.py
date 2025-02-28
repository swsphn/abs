from pathlib import Path
import polars as pl
from polars import col
import typer
from typing import Annotated

app = typer.Typer()


@app.command()
def ascceg(
    output: Annotated[
        Path, typer.Argument(help="directory or filepath to save output file (file suffix takes precedence over '-f' option)")
    ] = Path(),
    filetype: Annotated[str, typer.Option("--filetype", "-f", help="filetype ('parquet' or 'csv')")] = "parquet",
):
    ascceg_file = "https://www.abs.gov.au/statistics/classifications/australian-standard-classification-cultural-and-ethnic-groups-ascceg/2019/12490do0001_201912.xls"

    digits = r"^\d+$"

    main_groups = pl.read_excel(
        ascceg_file,
        sheet_name="Table 1.3",
        has_header=False,
        columns=[2, 3],
        read_options={"skip_rows": 9, "column_names": ["code", "group"]},
    ).filter(col("code").str.contains(digits))

    supplementary_groups = (
        pl.read_excel(
            ascceg_file,
            sheet_name="Table 2",
            has_header=False,
            columns=[0, 1],
            read_options={"skip_rows": 5, "column_names": ["code", "group"]},
        )
        .filter(col("code").str.contains(digits))
        .with_columns(col("code").str.pad_start(4, "0"))
    )

    all_groups = pl.concat([main_groups, supplementary_groups]).sort("code")

    if output.is_dir():
        output = output / f"ascceg.{filetype}"

    if output.suffix == ".parquet":
        all_groups.write_parquet(output)
    elif output.suffix == ".csv":
        all_groups.write_csv(output)
