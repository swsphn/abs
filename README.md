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

## Contributing

Here are the steps to add a new data source to this tool:

1.  Create a new module to fetch and transform the ABS data.
    1.  The module path should be `src/abs/<module>.py`, where
        `<module>` represents the name of the new module.
    2. This module MUST contain a function named `df()` which returns
       a [Polars][] DataFrame.
    3. This module SHOULD contain a docstring as the first line of the
       file.
    4. The module name will be automatically used as the name of the
       subcommand, and also of the output file.
2.  Update `__main__.py` to import the new module with `from abs import
    <module>`
3. Add the new subcommand to `__main__.py` with the `add_command(app,
   <module>)` function.

For example, suppose you create a new module called `sacc.py` to fetch
and tidy the [_Standard Australian Classification of Countries
(SACC)][sacc] data source. Assuming that you have added a docstring as
the first line of `sacc.py`, and have defined a function `df()` in
`sacc.py` which returns a Polars DataFrame, the only required steps to
create the CLI subcommand are to add the following two lines to
`__main__.py`:

``` python
from abs import sacc
add_command(app, sacc)
```

(Add the imports at the top of the file, and add the subcommands in the
appropriate location, with the other subcommands.)

[Polars]: https://pola.rs/
[Pandas]: https://pandas.pydata.org/
[to_pandas]: https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.to_pandas.html
[sacc]: https://www.abs.gov.au/statistics/classifications/standard-australian-classification-countries-sacc/2016#data-downloads
