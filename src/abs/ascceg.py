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

    # Load all sheets at once to avoid multiple downloads
    dfs = pl.read_excel(
        ascceg_file,
        sheet_name=["Table 1.1", "Table 1.2", "Table 1.3", "Table 2"],
        has_header=False,
    )

    broad_groups = (
        dfs["Table 1.1"]
        .with_row_index()
        .filter(col("index") >= 5)
        .select(col("column_1").alias("broad_code"), col("column_2").alias("broad_group"))
        .filter(col("broad_code").str.contains(digits))
    )

    narrow_groups = (
        dfs["Table 1.2"]
        .with_row_index()
        .filter(col("index") >= 7)
        .select(col("column_2").alias("narrow_code"), col("column_3").alias("narrow_group"))
        .filter(col("narrow_code").str.contains(digits))
    )

    main_groups = (
        dfs["Table 1.3"]
        .with_row_index()
        .filter(col("index") >= 9)
        .select(
            col("column_3").alias("code"),
            col("column_4").alias("cultural_and_ethnic_group"),
        )
        .filter(col("code").str.contains(digits))
    )

    supplementary_groups = (
        dfs["Table 2"]
        .with_row_index()
        .filter(col("index") >= 4)
        .select(
            col("column_1").alias("code"),
            col("column_2").alias("cultural_and_ethnic_group"),
        )
        .filter(col("code").str.contains(digits))
        .with_columns(col("code").str.pad_start(4, "0"))
    )

    all_groups = (
        pl.concat([main_groups, supplementary_groups])
        .join(broad_groups, left_on=col("code").str.slice(0, 1), right_on="broad_code", how='full')
        .join(narrow_groups, left_on=col("code").str.slice(0, 2), right_on="narrow_code", how='full')
        .select("code", "broad_group", "narrow_group", "cultural_and_ethnic_group")
        .sort("code")
    )

    return all_groups
