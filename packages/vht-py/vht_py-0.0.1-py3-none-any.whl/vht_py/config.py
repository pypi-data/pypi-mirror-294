#!/usr/bin/env python3
from argparse import Namespace
import pathlib
from loadconf import Config


class NoBaseDirExists(Exception):
    """Exception raised when user has a base directory set
    but it does not exist.
    """

    def __init__(self, config, message="ERROR: Base directory is set to"):
        self.file = config
        self.message = message

    def __str__(self):
        return f'{self.message} "{self.file}" which does not exist'


class NoBaseDir(Exception):
    """Exception raised when user has not set a base directory"""

    def __init__(self, config, message="ERROR: Base directory not set in"):
        self.file = config
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} "{self.file}"'


def get_user_settings(program, args) -> tuple[Config, Namespace]:
    # Create user object to read files and get settings
    user = Config(program=program)
    # Define some basic settings, files, etc.
    user_settings = {
        "base_dir": "~/Videos",
        "prompt_cmd": "fzf",
        "prompt_args": "",
        "file_manager": "",
        "trash_program": "trash",
        "confirm_delete": True,
        "debug": False,
        "wk_keywords": "+write",
        "wk_keys": "a s d f g h j k l ;",
        "wk_quit_key": "q",
        "wk_preprocessor_cmds": ":delay 0",
        "wk_cmd_prefix": "{{",
        "wk_cmd_suffix": "}}",
    }
    config_files = {
        "config": "vht.conf",
        "filters": "filters.conf",
        "library": "library.json",
        "library_backup": "library.json.bak",
    }
    files = [
        "config",
        "filters",
        "library",
    ]
    settings = list(user_settings)
    # Fill out user object
    user.define_settings(settings=user_settings)
    user.define_files(user_files=config_files)
    user.create_files(create_files=files)
    user.associate_settings(settings, "config")
    user.create_template(["config"])
    user.read_conf(user_settings=settings, read_files=["config"])
    user.store_files(files=["filters"])
    # Check that the required settings are defined
    try:
        if user.settings["base_dir"] is None:
            raise NoBaseDir(config=user.files["config"])
        elif not pathlib.Path(user.settings["base_dir"]).expanduser().resolve().is_dir():
            raise NoBaseDirExists(config=user.settings["base_dir"])
    except KeyError:
        raise NoBaseDir(config=user.files["config"])

    user.settings["confirm_delete"] = not args.no_confirm

    return user, args
