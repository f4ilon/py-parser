from parser import parse_value_by_title, parse_all_pairs

# Получить одно значение
value = parse_value_by_title("https://zakupki.gov.ru/epz/order/notice/notice223/common-info.html?regNumber=32616014089", "Способ осуществления закупки")
print(value)

# Получить все пары
all_data = parse_all_pairs("https://zakupki.gov.ru/epz/order/notice/notice223/common-info.html?regNumber=32616014089")
for title, value in all_data.items():
    print(f"{title}: {value}")