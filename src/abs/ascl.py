"""Fetch Australian Standard Classification of Languages
(ASCL) data from ABS.
"""

import polars as pl
from polars import col


def df():
    """Fetch Australian Standard Classification of Languages
    (ASCL) data from ABS.

    Return a tidy Polars DataFrame
    """
    ascceg_file = "https://www.abs.gov.au/statistics/classifications/australian-standard-classification-languages-ascl/2025/2025%20ASCL%20structure%201.0.xlsx"

    digits = r"^\d+$"

    # Load all sheets at once to avoid multiple downloads
    dfs = pl.read_excel(
        ascceg_file,
        sheet_name=["Table 1.1", "Table 1.2", "Table 1.3", "Table 1.4", "Table 2"],
        has_header=False,
    )

    language_family_groups = (
        dfs["Table 1.1"]
        .with_row_index()
        .filter(col("index") >= 5)
        .select(
            col("column_1").alias("language_family_code"),
            col("column_2").alias("language_family_group"),
        )
        .filter(col("language_family_code").str.contains(digits))
    )

    sub_family_groups = (
        dfs["Table 1.2"]
        .with_row_index()
        .filter(col("index") >= 5)
        .select(
            col("column_3").alias("sub_family_code"),
            col("column_4").alias("sub_family_group"),
        )
        .filter(col("sub_family_code").str.contains(digits))
    )

    narrow_groups = (
        dfs["Table 1.3"]
        .with_row_index()
        .filter(col("index") >= 5)
        .select(
            col("column_5").alias("narrow_code"), col("column_6").alias("narrow_group")
        )
        .filter(col("narrow_code").str.contains(digits))
    )

    main_groups = (
        dfs["Table 1.4"]
        .with_row_index()
        .filter(col("index") >= 5)
        .select(
            col("column_7").alias("code"),
            col("column_8").alias("language"),
        )
        .filter(col("code").str.contains(digits))
    )

    supplementary_groups = (
        dfs["Table 2"]
        .with_row_index()
        .filter(col("index") >= 4)
        .select(
            col("column_1").alias("code"),
            col("column_2").alias("language"),
        )
        .filter(col("code").str.contains(digits))
        .with_columns(col("code").str.pad_start(8, "0"))
    )

    all_groups = (
        pl.concat([main_groups, supplementary_groups])
        .join(
            language_family_groups,
            left_on=col("code").str.slice(0, 2),
            right_on="language_family_code",
            how="full",
        )
        .join(
            sub_family_groups,
            left_on=col("code").str.slice(0, 4),
            right_on="sub_family_code",
            how="full",
        )
        .join(
            narrow_groups,
            left_on=col("code").str.slice(0, 6),
            right_on="narrow_code",
            how="full",
        )
        .select(
            "code",
            "language_family_group",
            "sub_family_group",
            "narrow_group",
            "language",
        )
        .with_columns(col("language").str.strip_chars())
        .sort("code")
    )

    return all_groups
