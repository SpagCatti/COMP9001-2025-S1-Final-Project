"""
progress_manager.py
Manages user progress for JLPT levels in JapaneseStudy

References:
https://docs.python.org/3/library/csv.html
https://www.geeksforgeeks.org/python-os-makedirs-method/
"""


import csv
import os
from typing import Dict, Tuple, List, Set

import ui_handler as UI
import data_loader as DATA

PROGRESS_FILE = 'data/user_progress.csv'


def create_progress_file():
    """
    Creates an empty progress file.
    """
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'mastered_vocab'])
        for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
            writer.writerow([level])


def load_mastered_vocabs() -> Dict[str, Set[str]]:
    """
    Loads the vpcabulary items that the user has mastered for each level.

    Returns:
        Dict mapping JLPT levels to sets of mastered vocabulary kanji
    """
    mastery = {
        'N5': set(),
        'N4': set(),
        'N3': set(),
        'N2': set(),
        'N1': set()
    }

    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                if len(line) >= 2:
                    level = line[0]
                    vocabs = line[1:]
                    for vocab in vocabs:
                        if vocab.strip():
                            mastery[level].add(vocab)
        return mastery
    except FileNotFoundError:
        create_progress_file()
        return mastery


def add_mastered_vocab(level: str, kanji: str) -> bool:
    """
    Add a vocab to the user's mastered list.

    Args:
        level (str): JLPT level
        kanji (str): Kanji for the vocab

    Returns:
        True if added successfully. False otherwise.
    """
    mastery = load_mastered_vocabs()

    if kanji in mastery[level]:
        return False
    
    mastery[level].add(kanji)

    with open(PROGRESS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'mastered_vocab'])
        for level, vocab_set in mastery.items():
            row = [level] + list(vocab_set)
            writer.writerow(row)
    
    return True


def load_user_progress() -> Dict[str, tuple[int, int]]:
    """
    Loads user progress saved from the user_progress file.

    Returns:
        dict[str, tuple[int, int]]: A dictionary mapping JLPT levels to (mastered, total) tuples.
    """
    mastery = load_mastered_vocabs()
    user_progress = {}

    for level in mastery:
        mastered = len(mastery[level])

        all_vocab = DATA.load_jlpt_vocab(level)
        total = len(all_vocab)

        user_progress[level] = (mastered, total)
    
    return user_progress


def update_user_progress(level: str, mastered: int):
    """
    Update user progress on a specified JLPT level.

    Args:
        level (str): JLPT level as a string.
        mastered (int): The number of vocabs the user has answered correctly.
    """
    user_progress = load_user_progress()

    total = user_progress[level][1]
    user_progress[level] = (mastered, total)

    with open(PROGRESS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'mastered', 'total'])
        for level, (mastered, total) in user_progress.items():
            writer.writerow([level, mastered, total])


def reset_progress() -> bool:
    """
    Resets all JLPT levels progress.

    Returns:
        bool: True if reset was successful. False otherwise.
    """
    try:
        create_progress_file()
        return True
    except Exception as e:
        print(f'{UI.Colours.RED}Error resetting progress: {str(e)}{UI.Colours.END}')
        return False
