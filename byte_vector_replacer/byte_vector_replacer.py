#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4
# disable: byte-vector-replacer

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  # Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement
# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning
# pylint: disable=C0413  # TEMP isort issue [wrong-import-position] Import "from pathlib import Path" should be placed at the top of the module [C0413]

import os
import sys
import time
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
#from typing import ByteString
#from typing import Generator
#from typing import List
#from typing import Tuple
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import Union

import click
import sh
#from eprint import eprint
from asserttool import ic
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
#from with_sshfs import sshfs
#from with_chdir import chdir
from mptool import output
from replace_text import replace_text_in_file
from retry_on_exception import retry_on_exception
from timetool import get_timestamp
from unmp import unmp

sh.mv = None  # use sh.busybox('mv'), coreutils ignores stdin read errors

signal(SIGPIPE, SIG_DFL)

def get_pairs(verbose: Union[bool, int, float]) -> dict:
    pair_dict = \
    {
        b'verbose: bool,\n': b'verbose: Union[bool, int, float],\n',
        b'from enumerate_input import enumerate_input\n': b'from unmp import unmp\n',
        b'debug=debug,\n': None,
        b'debug=debug,': None,
        b' debug=debug': None,
        b'debug: bool,\n': None,
        b'debug: bool\n': None,
        b'debug: bool,': None,
        b'debug=self.debug': None,
        b'debug=False': None,
        b"debug=ctx.obj['debug']": None,
        b'debug: bool = False,\n': None,
        b'debug: bool = False\n': None,
        b'from iridb.click_global_options import add_options\n': None,
        b'from iridb.click_global_options import click_global_options\n': None,
        b'if debug:\n': b'if verbose == inf:\n',
        b'if self.debug:\n': b'if verbose == inf:\n',
        b'@click.option("--debug", is_flag=True)\n': b'@click_add_options(click_global_options)\n',
        b'verbose: bool = False,\n': b'verbose: Union[bool, int, float],\n',
        b'verbose: bool = False\n': b'verbose: Union[bool, int, float],\n',
        b'verbose: bool\n': b'verbose: Union[bool, int, float],\n',
        b'verbose: int,\n': b'verbose: Union[bool, int, float],\n',
        b'verbose=debug': b'verbose=verbose',
        b'@add_options(click_global_options)\n': b'@click_add_options(click_global_options)\n',
        b'@click.group()\n': b'@click.group(no_args_is_help=True)\n',
        b'from printtool import output\n': b'from mptool import output\n',
        b', ,': b',',
        b'verbose: int):\n': b'verbose: Union[bool, int, float],):\n',
        b'    verbose: int\n': b'    verbose: Union[bool, int, float]\n',
        b'from asserttool import eprint\n': b'from eprint import eprint\n',
        b'from asserttool import tv\n': b'from clicktool import tv\n',
    }
    return pair_dict


def byte_vector_replacer(*,
                         path: Path,
                         pair_dict: dict,
                         verbose: Union[bool, int, float],
                         ) -> None:

    guard = b'# disable: byte-vector-replacer\n'
    ic(guard)
    #all_bytes = path.read_bytes()
    if guard in path.read_bytes():
        raise ValueError(guard)
    assert False
    for key, value in pair_dict.items():
        ic(key, value)
        if value is None:
            value = b''
            remove_match = True
        else:
            remove_match = False
        replace_text_in_file(path=path,
                             bytes_to_match=key,
                             replacement=value,
                             output_fh=None,
                             stdout=False,
                             read_mode='rb',
                             write_mode='wb',
                             remove_match=remove_match,
                             verbose=True,
                             )


@click.command()
@click.argument("paths", type=str, nargs=-1)
@click.option('--ipython', is_flag=True)
@click_add_options(click_global_options)
@click.pass_context
def cli(ctx,
        paths: Sequence[str],
        ipython: bool,
        verbose: Union[bool, int, float],
        verbose_inf: bool,
        ) -> None:

    tty, verbose = tv(ctx=ctx,
                      verbose=verbose,
                      verbose_inf=verbose_inf,
                      )

    if paths:
        iterator = paths
    else:
        iterator = unmp(valid_types=[bytes,], verbose=verbose)
    del paths

    pair_dict = get_pairs(verbose=verbose)
    index = 0
    for index, path in enumerate(iterator):
        _path = Path(os.fsdecode(path))

        if verbose:
            ic(index, _path)

        if ipython:
            import IPython; IPython.embed()

    byte_vector_replacer(path=_path, pair_dict=pair_dict, verbose=verbose,)
