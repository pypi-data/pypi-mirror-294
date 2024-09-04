#!/usr/bin/env python3

from .system import return_cmd


def watch(files: list[str]):
    """
    Watch the given files.
    """

    cmd = ["mpv"]
    cmd.extend(files)

    return_cmd(cmd)
