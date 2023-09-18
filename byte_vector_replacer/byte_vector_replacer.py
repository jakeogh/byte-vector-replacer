#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4
# disable: byte-vector-replacer
# disable: black

# pylint: disable=useless-suppression             # [I0021]
# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-param-doc               # [W9015]
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement

import os
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import Union

import click
from asserttool import ic
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from replace_text import replace_text_in_file
from unmp import unmp

signal(SIGPIPE, SIG_DFL)

class GuardFoundError(ValueError):
    pass


#        b"verbose,\n": b"verbose: Union[bool, int, float],\n",
def get_pairs(verbose: Union[bool, int, float] = False,) -> dict:
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
        b" quit(": b" sys.exit(",
        b', "click-command-tree"': None,
        b"# pylint: disable=C0111  # docstrings are always outdated and wrong\n":            b"# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong\n",
        b"# pylint: disable=C0114  # Missing module docstring (missing-module-docstring)\n": b"# pylint: disable=missing-module-docstring        # [C0114]\n",
        b"# pylint: disable=W0511  # todo is encouraged\n":                                  b"# pylint: disable=fixme                           # [W0511] todo is encouraged\n",
        b"# pylint: disable=W0511  # todo encouraged\n":                                     b"# pylint: disable=fixme                           # [W0511] todo is encouraged\n",
        b"# pylint: disable=fixme  # [W0511] todo is encouraged\n":                          b"# pylint: disable=fixme                           # [W0511] todo is encouraged\n",
        b"# pylint: disable=C0301  # line too long\n":                                       b"# pylint: disable=line-too-long                   # [C0301]\n",
        b"# pylint: disable=R0902  # too many instance attributes\n":                        b"# pylint: disable=too-many-instance-attributes    # [R0902]\n",
        b"# pylint: disable=C0302  # too many lines in module\n":                            b"# pylint: disable=too-many-lines                  # [C0302] too many lines in module\n",
        b"# pylint: disable=C0103  # single letter var names, func name too descriptive\n":  b"# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive\n",
        b"# pylint: disable=R0911  # too many return statements\n":                          b"# pylint: disable=too-many-return-statements      # [R0911]\n",
        b"# pylint: disable=R0912  # too many branches\n":                                   b"# pylint: disable=too-many-branches               # [R0912]\n",
        b"# pylint: disable=R0915  # too many statements\n":                                 b"# pylint: disable=too-many-statements             # [R0915]\n",
        b"# pylint: disable=R0913  # too many arguments\n":                                  b"# pylint: disable=too-many-arguments              # [R0913]\n",
        b"# pylint: disable=R1702  # too many nested blocks\n":                              b"# pylint: disable=too-many-nested-blocks          # [R1702]\n",
        b"# pylint: disable=R0914  # too many local variables\n":                            b"# pylint: disable=too-many-locals                 # [R0914]\n",
        b"# pylint: disable=R0903  # too few public methods\n":                              b"# pylint: disable=too-few-public-methods          # [R0903]\n",
        b"# pylint: disable=E1101  # no member for base\n":                                  b"# pylint: disable=no-member                       # [E1101] no member for base\n",
        b"# pylint: disable=W0201  # attribute defined outside __init__\n":                  b"# pylint: disable=attribute-defined-outside-init  # [W0201]\n",
        b"# pylint: disable=R0916  # Too many boolean expressions in if statement\n":        b"# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement\n",
        b" Optional[list[str]] ": b" None | list[str] ",
        b" Optional[list[bytes]] ": b" None | list[bytes] ",
        b": Optional[List[bytes]]\n": b": None | list[bytes]\n",
        b": Optional[List[bytes]],\n": b": None | list[bytes],\n",
        b"Optional[bytes]": b"None | bytes",
        b"Optional[str]": b"None | str",
        b"Optional[int]": b"None | int",
        b"Optional[object]": b"None | object",
        b"Optional[dict]": b"None | dict",
        b"Optional[Digest]": b"None | Digest",
        b"Optional[bool]": b"None | bool",
        b"Optional[Path]": b"None | Path",
        b"Optional[list]": b"None | list",
        b"Optional[List]": b"None | list",
        b"from typing import Optional\n": None,
        b"from typing import Union\n": None,
        b"from typing import List\n": None,
        b"List[bytes]": b"list[bytes]",
        b"List[str]": b"list[str]",
        b"from typing import Iterator\n": b"from collections.abc import Iterator\n",
        b"Optional[Sequence[str]]": b"None | Sequence[str]",
        b"Optional[Sequence[Path]]": b"None | Sequence[Path]",
        b"Optional[tuple[str]]": b"None | tuple[str, ...]",
        b"from typing import Sequence\n": b"from collections.abc import Sequence\n",
        b"Union[int, str, Path]": b"int | str | Path",
        b"Union[str, bytes, object]": b"str | bytes | object",
        b"Union[dict, bool]": b"dict | bool",
        b"Union[str, bytes]": b"str | bytes",
        b"Optional[tuple[int, int]]": b"None | tuple[int, int]",
        b"Optional[Sequence[int]]": b"None | Sequence[int]",
        b"Union[bool, int, float]": b"bool | int | float",
        b"Union[list, tuple]": b"list | tuple",
        b"Optional[list | tuple]": b"None | list | tuple",
        b"from mptool import unmp": b"from unmp import unmp",
        b"# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning": None,
        b"# flake8: noqa           # flake8 has no per file settings :(": None,
        b"Optional[Decimal]": b"None | Decimal",
        b"Optional[Tuple[str, ...]]": b"None | Tuple[str, ...]",
        b"# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement\n\n\n": b"# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement\nfrom __future__ import annotations\n",
        b"Optional[Iterator[str]]": b"None | Iterator[str]",
        b"Optional[Iterable[str]]": b"None | Iterable[str]",
        b"Optional[Sequence]": b"None | Sequence",
        b"Optional[float]": b"None | float",
        b"Union[bytes, dict]": b"bytes | dict",
        b"Union[bool, float, int]": b"bool | int | float",
        b"@click.group(no_args_is_help=True)": b"@click.group(no_args_is_help=True, cls=AHGroup)",
        b"#!/usr/bin/env python3\n\n# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong\n": b"#!/usr/bin/env python3\n# -*- coding: utf8 -*-\n\n# pylint: disable=useless-suppression             # [I0021]\n# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong\n",
        b"dict_input": b"dict_output",
        b"verbose: bool | int | float,": b"verbose: bool | int | float = False,",
        b"from iridb.StatusLine import StatusLine": b"from statustool.StatusLine import StatusLine",
        b"verbose: bool | int | float = False,": b"verbose: bool,",
    }
    return pair_dict

# need a guard arg, like the :value cant already exist at all

# del Optional[Iterator[str]]

def byte_vector_replacer(
    *,
    path: Path,
    pair_dict: dict,
    verbose: Union[bool, int, float] = False,
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
            read_mode="rb",
            write_mode="wb",
            remove_match=remove_match,
        )


@click.command()
@click.argument("paths", type=str, nargs=-1)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    paths: tuple[str, ...],
    verbose_inf: bool,
    dict_output: bool,
    verbose: Union[bool, int, float] = False,
) -> None:

    if not verbose:
        ic.disable()

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
        try:
            byte_vector_replacer(
                path=_path,
                pair_dict=pair_dict,
                verbose=verbose,
            )
        except GuardFoundError as e:
            ic(e)
