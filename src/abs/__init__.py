# Automatically load data source definition modules.
# We wrap this in a function, then delete the function after use to
# avoid polluting the package namespace.
#
# The practical effect of this code is as follows:
#
# When a user runs `import abs`, all top-level modules except those
# starting with underscores will be imported.
#
# For example, given the following directory structure, there is
# a top-level module called 'ascceg.py'. It will be imported, and
# available at `abs.ascceg`:
#
# abs
# ├── ascceg.py
# ├── __init__.py
# └── __main__.py
#
# We also populate the __all__ variable. This provides an explicit list
# of the public submodules. This also specifies what will be imported
# with `from abs import *`.

# Ensure __all__ is in the global namespace
__all__ = []

def load_submodules():
    import importlib
    from pathlib import Path

    # get all sibling modules, except those starting with underscores
    module_paths = filter(
        lambda p: not p.name.startswith("_"), Path(__file__).parent.glob("*.py")
    )
    __all__.extend([p.stem for p in module_paths])

    # dynamically import all top-level modules whose names do not start with
    # underscores
    for module in __all__:
        globals()[module] = importlib.import_module(f".{module}", __name__)


load_submodules()

# Remove from package namespace
del load_submodules
