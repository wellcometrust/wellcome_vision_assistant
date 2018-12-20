import os

import requests

from utils import open_image, ocr
from settings import SLACK_OAUTH_TOKEN, SLACK_ADD_REMINDERS_ENDPOINT


def is_date(text):
    tokens = text.split() + [None]
    return tokens[0] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def text_to_menu_items(text):
    text_lines = text.split('\n')

    menu_items_indices = []
    for index, line in enumerate(text_lines):
        if is_date(line):
            menu_items_indices.append(index)
    
    menu_items = []
    for index in range(len(menu_items_indices)-1):
        start_index, end_index = menu_items_indices[index:index+2]
        date_component = text_lines[start_index]
        food_component = " ".join(text_lines[start_index+1:end_index])
        menu_items.append((date_component, food_component))
    return menu_items

def add_reminder(date, text):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'time': f"on {date}",
        'token': SLACK_OAUTH_TOKEN,
        'text': text,
    }
    response = requests.post(SLACK_ADD_REMINDERS_ENDPOINT, headers=headers, params=params)
    print(response.text)

def add_reminders(img_path):
    img = open_image(img_path)
    ocr_text = ocr(img)

    menu_items = text_to_menu_items(ocr_text)[:4]
    for date, food in menu_items:
        add_reminder(date, food)
    return menu_items
