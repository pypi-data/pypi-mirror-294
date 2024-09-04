#!/usr/bin/env python3
import argparse


def get_opts(prog_name="vht") -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""Video hash tracker""",
        allow_abbrev=False
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-u", "--update",
        action="store_true",
        help="Update the hash library, may take a long time."
    )
    group.add_argument(
        "-c", "--cleanup",
        action="store_true",
        help="Cleanup duplicates in the library."
    )
    # Need a way to cleanup dups...
    parser.add_argument(
        "-n", "--no-confirm",
        action="store_true",
        help="Don't confirm when cleaning dups."
    )
    parser.add_argument(
        "files",
        metavar="FILES",
        nargs=argparse.REMAINDER,
        default=[],
        help="Give files to add to vht without running a full update."
    )
    args = parser.parse_args()
    return args
