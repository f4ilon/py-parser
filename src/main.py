from pathlib import Path
from tqdm import tqdm
import tomllib
import time 
import sys


from parser import parse_value_by_title, parse_all_pairs
from xlsx import save_cell, cell_value, xlsx_info
from fs import get_xlsx


STD_CONFIG = """\
[settings]
sleep_time = 5
title = "text_title"\
"""

config = tomllib


def load_config():
    global config
    with open('config.toml', 'rb') as config_file:
        config = tomllib.load(config_file)
    print("config загружен")
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

    global config
    load_config()


def get_input_files():
    files = get_xlsx('input')
    if not files:
        print("Нет файлов для обработки.")
        input()
        exit()
    elif len(files) % 10 == 1:
        print(f"В очереди {len(files)} файл")
    elif len(files) % 10 <= 4:
        print(f"В очереди {len(files)} файла")
    else:
        print(f"В очереди {len(files)} файлов")
    return files


def parse(input_file):
    params = xlsx_info(input_file)
    if params[1] == 0:
        print(f"Файл {input_file.name} уже обработан")
        input_file.rename("output\\"+input_file.name)
        return

    for _ in tqdm(range(params[1]), desc=f"Обработка файла {input_file.name}", unit="%"):
        title_text = 'Способ осуществления закупки'
        url = cell_value(input_file, params[0])

        parse_result = parse_value_by_title(url, title_text)

        save_cell(input_file, params[0], parse_result)

        params[0][0] += 1
        time.sleep(config['settings']['sleep_time'])

    input_file.rename("output\\"+input_file.name)

    
def main():
    init()

    queue = get_input_files()

    for file in queue:
        parse(file)

    



if __name__ == '__main__':
    main()
