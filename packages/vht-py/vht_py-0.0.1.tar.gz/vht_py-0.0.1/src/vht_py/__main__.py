#!/usr/bin/env python3
from argparse import Namespace
from loadconf import Config
import sys


from .config import NoBaseDir, NoBaseDirExists, get_user_settings
from .library import update_library, add_files, clean_library
from .utils import cprint
from .options import get_opts


__license__ = "GPL-v3.0"
__program__ = "vht"


def process_opts(user: Config, args: Namespace):
    if args.files != []:
        cprint("green", "Adding file(s) to library.")
        return add_files(user, args.files)
    elif args.update:
        cprint("green", "Updating library.")
        return update_library(user)
    elif args.cleanup:
        cprint("green", "Cleaning up library duplicates.")
        return clean_library(user)

    cprint("yellow", f"No changes made. Try {__program__} --help for more info.")
    return 1


def main():
    args = get_opts(__program__)

    try:
        user, args = get_user_settings(__program__, args)
    except (NoBaseDir, NoBaseDirExists) as err:
        cprint("red", str(err), sys.stderr)
        return 1

    return process_opts(user, args)


if __name__ == "__main__":
    sys.exit(main())
