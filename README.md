# ABS

Python package to download data from the Australian Bureau of Statistics
(ABS) and process to tidy format.

It can be used either as a command-line tool, or as a library.

## Install

``` sh
pip install abs@git+https://github.com/swsphn/abs.git
pipx install abs@git+https://github.com/swsphn/abs.git
```

## CLI Usage

``` sh
# show available commands
abs --help

# show options for ascceg command
abs ascceg --help

# download ascceg file to current directory (defaults to parquet)
abs ascceg

# download ascceg file to a different directory as csv
abs ascceg -f csv some/other/directory

# download ascceg file with a specific name and filetype

abs ascceg some/file.csv
abs ascceg some/file.parquet
```

## Library Usage

You can also use this package as a library. Data is returned as tidy
[Polars][] DataFrames. If you are more comfortable with [Pandas][],
you can convert the DataFrame with the [to_pandas][] method.

``` python
import abs

ascceg = abs.ascceg.df()
print(ascceg)
```

[Polars]: https://pola.rs/
[Pandas]: https://pandas.pydata.org/
[to_pandas]: https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.to_pandas.html
