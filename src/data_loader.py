"""
data_loader.py
Manages data loading and saving operations for JapaneseStudy

References:
https://docs.python.org/3/library/csv.html
https://docs.python.org/3/library/datetime.html
"""


import csv
import os
from datetime import datetime
from typing import List, Dict, TypedDict

import ui_handler as UI


JLPT_FILES = {
    'N5': 'data/jlpt_n5.csv',
    'N4': 'data/jlpt_n4.csv',
    'N3': 'data/jlpt_n3.csv',
    'N2': 'data/jlpt_n2.csv',
    'N1': 'data/jlpt_n1.csv'
}


CHARACTER_FILE = 'data/characters.csv'
PROGRESS_FILE = 'data/user_progress.csv'
MISTAKES_FILE = 'data/mistakes.csv'


class Mistake(TypedDict):
    word: str
    kana: str
    correct_answer: str
    user_answer: str
    mistake_count: int
    last_mistake_date: str


def load_jlpt_vocab(level: str) -> List[Dict[str, str]]:
    """
    Load vocabulary from specified JLPT level file.
    
    Args:
        level (str): JLPT level as a string.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing specified JLPT level's vocab data. Returns an empty list if level does not exist.
    """
    vocab_list = []

    if level not in JLPT_FILES:
        return []
    
    try:
        with open(JLPT_FILES[level], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for vocab in reader:
                vocab_list.append(vocab)
        return vocab_list
    except FileNotFoundError:
        print(f'Task failed. {UI.Colours.YELLOW}jlpt_{level.lower()}.csv{UI.Colours.END} cannot be found.')

    
def load_characters() -> List[Dict[str, str]]:
    """
    Load japanese characters from the characters file.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing Japanese characters.
    """
    character_list = []

    try:
        with open(CHARACTER_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for character in reader:
                character_list.append(character)
        return character_list
    except FileNotFoundError:
        print(f'Task failed. {UI.Colours.YELLOW}{CHARACTER_FILE}{UI.Colours.END} cannot be found.')
