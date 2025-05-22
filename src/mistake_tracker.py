"""
mistake_tracker.py
Manages tracking and reviewing of user mistakes in JapaneseStudy

References:
https://docs.python.org/3/library/csv.html
"""


import csv
from datetime import datetime
from typing import List, Dict, TypedDict

import ui_handler as UI
import data_loader as DATA


MISTAKE_FILE = 'data/mistakes.csv'


class Mistake(TypedDict):
    """
    TypedDict for storing JLPT vocabulary mistake information.
    
    Fields:
        word: The Kanji shown in the question
        kana: The Kana pronunciation of the word
        correct_answer: The correct meaning that should have been chosen
        user_answer: The incorrect option that the user actually chose
    """
    word: str
    kana: str
    correct_answer: str
    user_answer: str


def load_mistakes() -> List[Mistake]:
    """
    Load user progress saved from the user_progress file.

    Returns:
        dict[str, str, str, str, int, str]: A dictionary containing user mistake details in the following format.
        - word (str)
        - kana (str)
        - correct_answer (str)
        - user_answer (str)
        - mistake_count (int)
        - last_mistake_date (str)
    """
    user_mistakes = []

    try:
        with open(MISTAKE_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for mistake in reader:
                mistake['mistake_count'] = int(mistake['mistake_count'])
                user_mistakes.append(mistake)
        return user_mistakes
    except FileNotFoundError:
        # TODO Create default progress file if can't find file.
        print(f'Task failed. {UI.Colours.YELLOW}{MISTAKE_FILE}{UI.Colours.END} cannot be found.')


def get_mistake_count() -> int:
    """
    Gets the total count of mistakes.

    Returns:
        int: Integer value of the total number of user mistakes.
    """
    return len(load_mistakes())


def add_mistake(word: str, kana: str, correct_answer: str, user_answer: str):
    """
    Adds a mistake in the mistakes file. If it already exists, increment mistake count by 1.

    Args:
        word (str): Japanese word
        kana (str): Kana representation
        correct_answer (str): The correct answer
        user_answer (str): User's incorrect answer
    """
    user_mistakes = load_mistakes()

    mistake_updated = False

    for mistake in user_mistakes:
        # If mistake already exists in the data bank, increment its count.
        if mistake['word'] == word and mistake['kana'] == kana:
            mistake['correct_answer'] = correct_answer
            mistake['user_answer'] = user_answer
            mistake['mistake_count'] += 1
            mistake['last_mistake_date'] = datetime.now().strftime('%y-%m-%d %H:%M:%S')
            mistake_updated = True
            break

    # If mistake does not exist in the data bank, add it.
    if not mistake_updated:
        user_mistakes.append({
            'word': word,
            'kana': kana,
            'correct_answer': correct_answer,
            'user_answer': user_answer,
            'mistake_count': 1,
            'last_mistake_date': datetime.now().strftime('%y-%m-%d %H:%M:%S')
        })

    with open(MISTAKE_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['word', 'kana', 'correct_answer', 'user_answer', 'mistake_count', 'last_mistake_date'])
        writer.writeheader()
        writer.writerows(user_mistakes)


def remove_mistake(word: str) -> bool:
    """
    Removes a mistake from the mistake data bank.

    Args:
        word (str): Japanese word

    Returns:
        Boolean: True if mistake has been removed successfully. False otherwise.
    """
    user_mistakes = load_mistakes()
    old_mistake_count = len(user_mistakes)

    # Remove the mistake from the list.
    filtered_mistakes = []
    for mistake in user_mistakes:
        if mistake['word'] != word:
            filtered_mistakes.append(mistake)

    # Write and save the new mistake list
    with open(MISTAKE_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['word', 'kana', 'correct_answer', 'user_answer', 'mistake_count', 'last_mistake_date'])
        writer.writeheader()
        writer.writerows(filtered_mistakes)

    return len(user_mistakes) < old_mistake_count


def reset_mistakes() -> bool:
    """
    Clears all saved mistakes.

    Returns:
        True if reset successfully. False otherwise.
    """
    try:
        with open(MISTAKE_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'kana', 'correct_answer', 'user_answer', 'mistake_count', 'last_mistake_date'])
        
        mistake_count = len(load_mistakes())
        return True
    
    except Exception as e:
        print(f'{UI.Colours.RED}Error resetting progress: {str(e)}{UI.Colours.END}')
        return False