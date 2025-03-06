"""Fetch Australian Standard Classification of Cultural and Ethnic
Groups (ASCCEG) data from ABS.
"""

import polars as pl
from polars import col


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
