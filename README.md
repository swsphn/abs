# ABS Data

Python package to download from ABS and process to tidy format.

## Install

``` sh
pip install abs-data@git+https://github.com/swsphn/abs-data.git
pipx install abs-data@git+https://github.com/swsphn/abs-data.git
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

You can also use this package as a library.

``` python
import abs

ascceg = abs.ascceg.df()
print(ascceg)
```
