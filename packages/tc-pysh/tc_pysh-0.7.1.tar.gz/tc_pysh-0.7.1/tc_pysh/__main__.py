import sys

from typing import Union, Callable

from . import *
from .path import *
from .file import *
from .file import head as _head
from .file import tail as _tail
from .file import skip as _skip
from .file import before as _before
from .file import grep as _grep
from . import ls as _ls
from . import find as _find
from . import cd as _cd
from .path import cwd as _cwd
from .command import Command
from .interpreter import Interpreter

ls = Command(_ls)
find = Command(_find)
cd = Command(_cd)
cwd = Command(_cwd)
head = Command(_head)
tail = Command(_tail)
skip = Command(_skip)
before = Command(_before)
grep = Command(_grep)


def main():
    interp.interact()


def set_ps1(prompt: Union[str, Callable]):
    if callable(prompt):

        class P:
            def __str__(self):
                return prompt()

        sys.ps1 = P()
    else:
        sys.ps1 = prompt


interp = Interpreter(local=locals())


if __name__ == "__main__":
    main()
