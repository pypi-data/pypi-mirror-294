#!/usr/bin/env python3

import hashlib
import json
from loadconf import Config
import pathlib
import re
import shutil

from .media import watch
from .prompts import user_choice
from .system import open_process
from .utils import cprint


def backup_library(user: Config):
    library = pathlib.Path(user.files["library"])
    backup = pathlib.Path(user.files["library_backup"])
    if not library.is_file():
        library.touch()
    else:
        shutil.copy(library, backup)

def compile_filters(filters: list[str]):
    pattern = f"({'|'.join(filters)})"
    return re.compile(pattern)


def is_filtered(dir: pathlib.Path, filters: re.Pattern):
    return bool(filters.search(str(dir.resolve()) + "/"))


def get_files(base_path: pathlib.Path, filters: re.Pattern) -> list[pathlib.Path]:
    files = []

    for item in base_path.glob("*"):
        if item.is_file():
            files.append(item)
        elif item.is_dir() and not is_filtered(item, filters):
            files.extend(get_files(item, filters))

    return files


def get_hash(file: str) -> str:
    hash = hashlib.sha256()

    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash.update(byte_block)

    return hash.hexdigest()


def get_hashes(files: list[pathlib.Path]) -> dict[str, list[str]]:
    hashes = {}

    for file in files:
        hash = get_hash(str(file))
        if hash in hashes:
            hashes[hash].append(str(file))
        else:
            hashes[hash] = [str(file)]

    return hashes

def update_library(user: Config):
    backup_library(user)

    filters = compile_filters(user.stored["filters"])
    files = get_files(
        pathlib.Path(user.settings["base_dir"]).expanduser().resolve(),
        filters
    )

    hashes = get_hashes(files)

    with open(user.files["library"], "w") as library:
        json.dump(hashes, library, indent=4)

    return 0


def add_files(user: Config, args: list[str]):
    backup_library(user)

    filters = compile_filters(user.stored["filters"])
    files = []

    for arg in args:
        item = pathlib.Path(arg).expanduser().resolve()
        if item.is_dir():
            files.extend(get_files(item, filters))
        else:
            files.append(item)

    hashes = get_hashes(files)

    with open(user.files["library"], "r") as data:
        library = json.load(data)

    for hash, matches in hashes.items():
        contents = set(library.get(hash, []))
        library[hash] = list(contents.union(set(matches)))

    with open(user.files["library"], "w") as data:
        json.dump(library, data, indent=4)

    return 0


def handle_dups(user: Config, dups: dict[str, list[str]]):

    for hash, files in list(dups.items()):
        # Remove any non-existant files
        files = [file for file in files if pathlib.Path(file).exists()]
        files.sort()
        dups[hash] = files
        keep = ""

        if user.settings["confirm_delete"] and len(files) > 1:
            watch(files)
            keep = user_choice(files, user, "Keep? ", offset=0)
        elif len(files) > 0:
            keep = files[0]

        # User wants to stop cleaning
        if keep == "*quit*":
            cprint("yellow", "Quiting...")
            break

        # There are dups to clean
        if keep != "":
            dups[hash] = [keep]
            for file in files:
                if file != keep:
                    open_process([user.settings["trash_program"], file])

    return dups


def clean_library(user: Config):
    library = {}

    with open(user.files["library"], "r") as data:
        library = json.load(data)

    dups = {hash: files for hash, files in library.items() if len(files) > 1}

    library.update(handle_dups(user, dups))

    backup_library(user)

    with open(user.files["library"], "w") as data:
        json.dump(library, data, indent=4)

    return 0
