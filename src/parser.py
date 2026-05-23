"""
Парсер для извлечения значений по заголовкам с веб-страницы.
Принимает URL и заголовок (common-text__title), возвращает значение (common-text__value).
"""

import requests
from bs4 import BeautifulSoup
import argparse
import sys


def parse_value_by_title(url: str, title_text: str) -> str | None:
    """
    Парсит страницу и находит common-text__value по common-text__title.
    
    Args:
        url: URL страницы для парсинга
        title_text: Текст заголовка для поиска
        
    Returns:
        Найденное значение или None
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}", file=sys.stderr)
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Способ 1: Ищем элемент с классом common-text__title и нужным текстом
    title_elements = soup.find_all(class_='common-text__title')
    
    for title_elem in title_elements:
        if title_text.lower() in title_elem.get_text(strip=True).lower():
            # Ищем связанный value в том же родителе
            parent = title_elem.parent
            value_elem = parent.find(class_='common-text__value')
            
            if value_elem:
                return value_elem.get_text(strip=True)
            
            # Если не нашли в прямом родителе, ищем в соседях
            sibling = title_elem.find_next_sibling(class_='common-text__value')
            if sibling:
                return sibling.get_text(strip=True)
            
            # Ищем следующий элемент с нужным классом
            next_value = title_elem.find_next(class_='common-text__value')
            if next_value:
                return next_value.get_text(strip=True)
    
    return None


def parse_all_pairs(url: str) -> dict:
    """
    Извлекает все пары title-value со страницы.
    
    Args:
        url: URL страницы
        
    Returns:
        Словарь {title: value}
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}", file=sys.stderr)
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    result = {}
    
    # Ищем все контейнеры с парами title-value
    title_elements = soup.find_all(class_='common-text__title')
    
    for title_elem in title_elements:
        title_text = title_elem.get_text(strip=True)
        
        # Пробуем разные стратегии поиска value
        parent = title_elem.parent
        value_elem = parent.find(class_='common-text__value') if parent else None
        
        if not value_elem:
            value_elem = title_elem.find_next(class_='common-text__value')
        
        if value_elem:
            result[title_text] = value_elem.get_text(strip=True)
    
    return result

