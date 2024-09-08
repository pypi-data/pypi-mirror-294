from .path import *
from .utils import *
from .file import open


__version__ = "0.7.0"


# I use that for the automatic doc
__all__ = [
    "AbsolutePath",
    "archive",
    "cat",
    "cd",
    "cp",
    "cwd",
    "ensure_abs_path",
    "ensure_path",
    "find",
    "in_dir",
    "ls",
    "mkdir",
    "mv",
    "open",
    "Query",
    "RelativePath",
    "rm",
    "sh",
    "sh_with_stdout",
]
