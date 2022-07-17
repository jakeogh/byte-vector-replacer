#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4
# disable: byte-vector-replacer
# disable: black

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

import os
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import Sequence
from typing import Union

import click
from asserttool import ic
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from mptool import unmp
from replace_text import replace_text_in_file

signal(SIGPIPE, SIG_DFL)


class GuardFoundError(ValueError):
    pass


def get_pairs(verbose: Union[bool, int, float]) -> dict:
    pair_dict = {
        b"verbose: bool,\n": b"verbose: Union[bool, int, float],\n",
        b"from enumerate_input import enumerate_input\n": b"from unmp import unmp\n",
        b"debug=debug,\n": None,
        b"debug=debug,": None,
        b" debug=debug": None,
        b"debug: bool,\n": None,
        b"debug: bool\n": None,
        b"debug: bool,": None,
        b"debug=self.debug": None,
        b"debug=False": None,
        b"debug=ctx.obj['debug']": None,
        b"debug: bool = False,\n": None,
        b"debug: bool = False\n": None,
        b"from iridb.click_global_options import add_options\n": None,
        b"from iridb.click_global_options import click_global_options\n": None,
        b"if debug:\n": b"if verbose == inf:\n",
        b"if self.debug:\n": b"if verbose == inf:\n",
        b'@click.option("--debug", is_flag=True)\n': b"@click_add_options(click_global_options)\n",
        b"verbose: bool = False,\n":            b"verbose: Union[bool, int, float],\n",
        b"verbose: bool = False\n":             b"verbose: Union[bool, int, float],\n",
        b"verbose: bool\n":                     b"verbose: Union[bool, int, float],\n",
        b"verbose: int,\n":                     b"verbose: Union[bool, int, float],\n",
        b"verbose: int,":                       b"verbose: Union[bool, int, float],",
        b"verbose: Union[bool, int],\n":        b"verbose: Union[bool, int, float],\n",
        b"verbose: int):\n":                    b"verbose: Union[bool, int, float],):\n",
        b"    verbose: int\n":                  b"    verbose: Union[bool, int, float]\n",
        b"verbose: Union[bool, int, float],\n": b"verbose: bool | int | float,\n",
        b"verbose: Union[bool, int, float]\n":  b"verbose: bool | int | float\n",
        b"verbose=debug": b"verbose=verbose",
        b"@add_options(click_global_options)\n": b"@click_add_options(click_global_options)\n",
        b"@click.group()\n": b"@click.group(no_args_is_help=True)\n",
        b"from printtool import output\n": b"from mptool import output\n",
        b", ,": b",",
        b"from asserttool import eprint\n": b"from eprint import eprint\n",
        b"from asserttool import tv\n": b"from clicktool import tv\n",
        b"from asserttool import nevd\n": b"from clicktool import tv\n",
        b"verbose: int = False,\n": b"verbose: Union[bool, int, float],\n",
        b"from typimg import ": b"from typing import ",
        b"from typimg import ": b"from typing import ",
        b"from unmp import unmp\n": b"from mptool import unmp\n",
        b" quit(": b" sys.exit(",
        b', "click-command-tree"': None,
        b"# pylint: disable=C0111  # docstrings are always outdated and wrong\n":           b"# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong\n",
        b"# pylint: disable=W0511  # todo is encouraged\n":                                 b"# pylint: disable=fixme                           # [W0511] todo is encouraged\n",
        b"# pylint: disable=W0511  # todo encouraged\n":                                    b"# pylint: disable=fixme                           # [W0511] todo is encouraged\n",
        b"# pylint: disable=fixme  # [W0511] todo is encouraged\n":                         b"# pylint: disable=fixme                           # [W0511] todo is encouraged\n",
        b"# pylint: disable=C0301  # line too long\n":                                      b"# pylint: disable=line-too-long                   # [C0301]\n",
        b"# pylint: disable=R0902  # too many instance attributes\n":                       b"# pylint: disable=too-many-instance-attributes    # [R0902]\n",
        b"# pylint: disable=C0302  # too many lines in module\n":                           b"# pylint: disable=too-many-lines                  # [C0302] too many lines in module\n",
        b"# pylint: disable=C0103  # single letter var names, func name too descriptive\n": b"# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive\n",
        b"# pylint: disable=R0911  # too many return statements\n":                         b"# pylint: disable=too-many-return-statements      # [R0911]\n",
        b"# pylint: disable=R0912  # too many branches\n":                                  b"# pylint: disable=too-many-branches               # [R0912]\n",
        b"# pylint: disable=R0915  # too many statements\n":                                b"# pylint: disable=too-many-statements             # [R0915]\n",
        b"# pylint: disable=R0913  # too many arguments\n":                                 b"# pylint: disable=too-many-arguments              # [R0913]\n",
        b"# pylint: disable=R1702  # too many nested blocks\n":                             b"# pylint: disable=too-many-nested-blocks          # [R1702]\n",
        b"# pylint: disable=R0914  # too many local variables\n":                           b"# pylint: disable=too-many-locals                 # [R0914]\n",
        b"# pylint: disable=R0903  # too few public methods\n":                             b"# pylint: disable=too-few-public-methods          # [R0903]\n",
        b"# pylint: disable=E1101  # no member for base\n":                                 b"# pylint: disable=no-member                       # [E1101] no member for base\n",
        b"# pylint: disable=W0201  # attribute defined outside __init__\n":                 b"# pylint: disable=attribute-defined-outside-init  # [W0201]\n",
        b"# pylint: disable=R0916  # Too many boolean expressions in if statement\n":       b"# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement\n",
        b" Optional[list[str]] ": b" None | list[str] ",
        b" Optional[list[bytes]] ": b" None | list[bytes] ",
        b": Optional[List[bytes]]\n": b": None | list[bytes]\n",
        b": Optional[List[bytes]],\n": b": None | list[bytes],\n",
        b"Optional[bytes]": b"None | bytes",
        b"Optional[str]": b"None | str",
        b"from typing import Optional\n": None,
        b"from typing import Union\n": None,
        b"from typing import List\n": None,
        b"List[bytes]": b"list[bytes]",
        b"List[str]": b"list[str]",
        b"from typing import Iterator\n": b"from collections.abc import Iterator\n",
        b"Optional[Sequence[str]]": b"None | Sequence[str]",
        b"Optional[Sequence[Path]]": b"None | Sequence[Path]",
        b"Optional[tuple[str]]":    b"None | tuple[str]",
        b"from typing import Sequence\n": b"from collections.abc import Sequence\n",
    }
    return pair_dict


def byte_vector_replacer(
    *,
    path: Path,
    pair_dict: dict,
    verbose: Union[bool, int, float],
) -> None:

    guard = b"# disable: byte-vector-replacer\n"
    ic(guard)
    if guard in path.read_bytes():
        raise GuardFoundError(path.as_posix(), guard)
    for key, value in pair_dict.items():
        if verbose:
            ic(key, value)
        if value is None:
            value = b""
            remove_match = True
        else:
            remove_match = False
        replace_text_in_file(
            path=path,
            match_bytes=key,
            replacement_bytes=value,
            output_fh=None,
            stdout=False,
            read_mode="rb",
            write_mode="wb",
            remove_match=remove_match,
            verbose=True,
        )


@click.command()
@click.argument("paths", type=str, nargs=-1)
@click.option("--ipython", is_flag=True)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    paths: Sequence[str],
    ipython: bool,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
) -> None:

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    if paths:
        iterator = paths
    else:
        iterator = unmp(
            valid_types=[
                bytes,
            ],
            verbose=verbose,
        )
    del paths

    pair_dict = get_pairs(verbose=verbose)
    index = 0
    for index, path in enumerate(iterator):
        _path = Path(os.fsdecode(path))

        if verbose:
            ic(index, _path)

        if ipython:
            import IPython

            IPython.embed()
        try:
            byte_vector_replacer(
                path=_path,
                pair_dict=pair_dict,
                verbose=verbose,
            )
        except GuardFoundError as e:
            ic(e)
