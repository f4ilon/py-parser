from pathlib import Path
import tomllib

from parser import parse_value_by_title, parse_all_pairs
from xlsx import start_parser
from fs import get_xlsx


STD_CONFIG = """\
[settings]
debug = true
TTS = 60
title = "text_title"\
"""


def get_config():
    with open('config.toml', 'rb') as config_file:
        config = tomllib.load(config_file)
    return config


def init():
    folder = Path("input")
    folder.mkdir(exist_ok=True)
    folder = Path("output")
    folder.mkdir(exist_ok=True)

    config_file = Path("config.toml")
    if not config_file.exists():
        config_file.write_text(STD_CONFIG, encoding="utf-8")
        print("config.toml создан")
    else:
        print("config.toml найден")


def get_input_files():
    files = get_xlsx('input')
    return files


if __name__ == '__main__':
    init()
    config = get_config()
    # print(config['settings']['title'])

    queue = get_input_files()
    