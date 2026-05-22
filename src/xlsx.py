from openpyxl import load_workbook
import random
import time
import sys
import os

from parser import parse_value_by_title, parse_all_pairs
title_text = 'Способ осуществления закупки'


def start_parser(input_file: str, output_file: str = None):
    # Загружаем файл
    wb = load_workbook(input_file)
    ws = wb.active

    start_row = 1
    urls_col = 1
    for col in range(1, ws.max_row + 1):
        if ws.cell(row=1, column=col).value == None:
            continue
        for row in range(1, ws.max_row + 1):
            if ws.cell(row=row, column=col).value[:8] == 'https://':
                start_row = row
                urls_col = col
                break

    target_col = urls_col+1

    for row in range(start_row, ws.max_row + 1):
        url = ws.cell(row=row, column=urls_col).value
        value = parse_value_by_title(url, title_text)
        if (value):
            ws.cell(row=row, column=target_col).value = value
        else:
            ws.cell(row=row, column=target_col).value = '>/<'
        time.sleep(random.uniform(45, 75))


    # Если имя выходного файла не указано — создаём автоматически
    if not output_file:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_parsed{ext}"

    wb.save(output_file)
    print(f"✅ Готово! Файл сохранён как: {output_file}")



