#!/usr/bin/env python3
from loadconf import Config
from promptx import PromptX

p = None

class InvalidCmdPrompt(Exception):
    """Exception raised when user has invalid command prompt"""

    def __init__(self, error, message="ERROR: prompt_cmd not recognized"):
        self.error = error
        self.message = message

    def __str__(self):
        return f'{self.message} "{self.error}"'


class InputError(Exception):
    """Exception fzf or dmenu prompt fails"""

    def __init__(self, error, message="ERROR: Could not get user input", prefix=""):
        self.error = error
        self.prefix = prefix
        self.message = message

    def __str__(self):
        return f"{self.prefix}{self.message}{self.error}"


def build_wks_description(cmd: str):
    return cmd.split("/")[-1]


def init_prompt(user: Config) -> PromptX:
    global p

    if p is None:
        p = PromptX(user.settings["prompt_cmd"])

        if user.settings["prompt_cmd"] == "wk":
            p.set_wk_preprocessor_cmds([user.settings["wk_preprocessor_cmds"]])
            p.set_wk_keywords([user.settings["wk_keywords"]])
            p.set_wk_keys(user.settings["wk_keys"])
            p.set_wk_quit_key(user.settings["wk_quit_key"])
            p.set_wk_cmd_prefix(user.settings["wk_cmd_prefix"])
            p.set_wk_cmd_suffix(user.settings["wk_cmd_suffix"])
            p.set_build_wks_description(build_wks_description)

    return p


def user_choice(
    options: list[str],
    user: Config,
    prompt: str,
    offset: int = 0,
) -> str:
    """
    Give user a prompt to choose from a list of options.  Uses dmenu, fzf, or
    rofi
    """
    cmd = user.settings["prompt_cmd"]
    cmd_args = user.settings["prompt_args"]
    p = init_prompt(user)
    if cmd == "dmenu" and cmd_args == "":
        cmd_args = "-l 20 -i"

    choice = p.ask(
        options=options,
        prompt=prompt,
        additional_args=cmd_args,
        offset=offset
    )

    def wk_process_choice(choice: list[str], offset: int):
        if choice[0] == p.get_wk_next_cmd():
            offset += p.get_wk_keys_len()
            return wk_process_choice(
                p.ask(options, prompt, cmd_args, offset=offset),
                offset
            )
        elif choice[0] == p.get_wk_prev_cmd():
            offset -= p.get_wk_keys_len()
            return wk_process_choice(
                p.ask(options, prompt, cmd_args, offset=offset),
                offset
            )
        elif choice[0] == p.get_wk_quit_cmd():
            return "*quit*"
        return choice[0]

    if cmd == "wk" and len(choice) > 0:
        return wk_process_choice(choice, offset)

    try:
        return choice[0]
    except IndexError:
        return ""
