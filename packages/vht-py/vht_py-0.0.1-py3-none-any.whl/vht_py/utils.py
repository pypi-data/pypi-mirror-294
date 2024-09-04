#!/usr/bin/env python3
import sys


def cprint(color: str, string, out_file=sys.stdout):
    """
    Red: \033[31m
    Green: \033[32m
    Yellow: \033[33m
    Blue: \033[34m
    Magenta: \033[35m
    Cyan: \033[36m
    """
    format = ""
    end = "\033[0m"
    if color.lower() == "red":
        format = "\033[31m"
    elif color.lower() == "green":
        format = "\033[32m"
    elif color.lower() == "yellow":
        format = "\033[33m"
    elif color.lower() == "blue":
        format = "\033[34m"
    elif color.lower() == "magenta":
        format = "\033[35m"
    elif color.lower() == "cyan":
        format = "\033[36m"
    else:
        print(string, file=out_file)
        return
    print(format + string + end, file=out_file)
