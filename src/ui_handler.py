"""
ui_handler.py
Manages user interface elements for JapaneseStudy

References:
https://www.geeksforgeeks.org/print-colors-python-terminal/
https://docs.python.org/3/tutorial/inputoutput.html
"""


import os
import time
from typing import List, Dict, TypedDict

import data_loader as DATA
import ui_handler as UI


class Colours:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Options(TypedDict):
    A: str
    B: str
    C: str
    D: str


def get_user_choice(prompt: str, valid_options: list[str]) -> str:
    """
    Gets a valid input from the user.
    
    Args:
        prompt (str): User's choice based on the menu.
        valid_options (list[str]): List of options that are accepted in the current scenario.

    Returns:
        str: The user's valid choice as a string.
    """
    while True:
        choice = input(prompt).strip()

        # Uppercase all user input to make it more user friendly
        choice = choice.upper()
        valid_options = [str(option).upper() for option in valid_options]

        # Return a string value if input is valid
        if choice in valid_options:
            return choice
        
        print(f'{Colours.RED}Invalid choice. Please try again.{Colours.END}')


def display_title(title: str):
    """
    Displays the title in a fixed format.

    Args:
        title (str): Title of the game to display.

    Returns:
        None
    """
    border = '(◡‿◡✿)' + '-' * (len(title)) + '(◕▿◕✿)'
    print()
    print(f'{Colours.BLUE}{border}{Colours.END}')
    print(f'Welcome to {Colours.BOLD}{title}{Colours.END}!')
    print(f'{Colours.BLUE}{border}{Colours.END}')


def display_main_menu(mistake_count: int) -> int:
    """
    Displays the main menu and prompts the user for a choice.

    Args:
        mistake_count (int): The number of mistakes stored in the mistake bank.

    Returns:
        int: The user's choice of action in the main menu as an integer (1-5).
    """
    print(f'\n{UI.Colours.CYAN}Please choose what you want to do today!{UI.Colours.END}\n')
    print(f'1. {Colours.BOLD}JLPT Quiz{Colours.END}')
    print(f'2. {Colours.BOLD}Character Quiz{Colours.END}')
    print(f'3. {Colours.BOLD}Learn the Vocabs{Colours.END}')
    print(f'4. {Colours.BOLD}Learn the Characters{Colours.END}')
    if mistake_count == 1:
        print(f'5. {Colours.BOLD}Mistake Practice{Colours.END} [{Colours.YELLOW}{mistake_count} mistake right now!{Colours.END}]')
    else:
        print(f'5. {Colours.BOLD}Mistake Practice{Colours.END} [{Colours.YELLOW}{mistake_count} mistakes right now!{Colours.END}]')
    print(f'6. {Colours.BOLD}Reset{Colours.END}')
    print(f'7. {Colours.BOLD}Quit{Colours.END}')
    print()
    return get_user_choice('Choice | ', range(1, 8))


def display_jlpt_quiz_menu(progress: Dict[str, tuple[int, int]]) -> int:
    """
    Displays the JLPT Quiz menu and prompts the user for a choice.

    Args:
        progress (dict[str, int]): A dictionary containing each JLPT level and their corresponding mastery level.

    Returns:
        int: The user's choice of action in the main menu as an integer (1-5).
    """
    score = progress['N5'][0]

    print(f'\n{Colours.BLUE}{Colours.BOLD}JLPT Quiz{Colours.END}')
    print(f'{Colours.CYAN}Please choose your proficiency level!{Colours.END}\n')
    print(f'1. {Colours.BOLD}N5{Colours.END} [{Colours.GREEN}{progress['N5'][0]}{Colours.END}/{progress['N5'][1]} mastered!]')
    print(f'2. {Colours.BOLD}N4{Colours.END} [{Colours.GREEN}{progress['N4'][0]}{Colours.END}/{progress['N4'][1]} mastered!]')
    print(f'3. {Colours.BOLD}N3{Colours.END} [{Colours.GREEN}{progress['N3'][0]}{Colours.END}/{progress['N3'][1]} mastered!]')
    print(f'4. {Colours.BOLD}N2{Colours.END} [{Colours.GREEN}{progress['N2'][0]}{Colours.END}/{progress['N2'][1]} mastered!]')
    print(f'5. {Colours.BOLD}N1{Colours.END} [{Colours.GREEN}{progress['N1'][0]}{Colours.END}/{progress['N1'][1]} mastered!]')
    print(f"...or enter 'r' to return to the previous menu!")
    print()
    return get_user_choice('Choice | ', ['1', '2', '3', '4', '5', 'R'])


def display_quiz_tips():
    """
    Displays guidance for answering the questions.
    """
    print(f'{Colours.BOLD}Tips:{Colours.BOLD}')
    print(f'- Inputs are {Colours.BOLD}NOT{Colours.END} case-sensitive! (e.g. You can enter a or A.)')
    print(f'- You can input {Colours.BOLD}q{Colours.END} or {Colours.BOLD}Q{Colours.END} to quit the current quiz and return to the main menu.')
    print(f'  [{Colours.RED}WARNING: THIS WILL NULLIFY THIS QUIZ ATTEMPT{Colours.END}]')
    print()


def display_jlpt_vocab_menu():
    """
    Displays the menu of JLPT levels for the user to select which level's vocab to see.

    Returns:
        str: A string value representing selected JLPT level or 'return' to go back
    """
    print(f'\n{Colours.BLUE}{Colours.BOLD}Learn the Vocabs{Colours.END}')
    print(f'{Colours.CYAN}Please choose which level vocabulary you want to learn!{Colours.END}')
    print(f'1. {Colours.BOLD}N5{Colours.END} (Beginner)')
    print(f'2. {Colours.BOLD}N4{Colours.END} (Basic)')
    print(f'3. {Colours.BOLD}N3{Colours.END} (Intermediate)')
    print(f'4. {Colours.BOLD}N2{Colours.END} (Upper-Intermediate)')
    print(f'5. {Colours.BOLD}N1{Colours.END} (Advanced)')
    print(f"...or enter '{Colours.BOLD}r{Colours.END}' to return to the Main Menu!")
    print()
    
    choice = get_user_choice('Choice | ', ['1', '2', '3', '4', '5', 'R'])
    
    # Map numeric choice to level
    level_map = {
        '1': 'N5',
        '2': 'N4', 
        '3': 'N3',
        '4': 'N2',
        '5': 'N1',
        'R': 'return'
    }
    
    return level_map.get(choice, 'return')


def display_vocabulary(level: str):
    """
    Displays all vocabs for learning without quiz functionality.

    Arg:
        level (str): A string representing the JLPT Level
    """
    vocabulary = DATA.load_jlpt_vocab(level)

    if not vocabulary:
        print(f"{UI.Colours.RED}No vocabulary data found for {level}!{UI.Colours.END}")
        return
    
    print(f"\n{UI.Colours.BLUE}{UI.Colours.BOLD}Learn JLPT {level} Vocabulary{UI.Colours.END}")
    print(f"{UI.Colours.CYAN}Here are all the {level} vocabularies and their pronunciations:{UI.Colours.END}\n")

    num_columns = 2
    vocab_per_column = (len(vocabulary) + num_columns - 1) // num_columns

    column_width = 55

    for line in range(vocab_per_column):
        line_output = ''
        for col in range(num_columns):
            index = line + col * vocab_per_column
            if index < len(vocabulary):
                vocab = vocabulary[index]
                item_num = index + 1
                
                vocab_text = f'{item_num:2d}. {Colours.PURPLE}{vocab['Kanji']}{Colours.END}'
                if 'Kana' in vocab and vocab['Kana']:
                    vocab_text += f' ({vocab['Kana']})'
                vocab_text += f' - {Colours.GREEN}{vocab['Meaning']}{Colours.END}'

                plain_text = f"{item_num:2d}. {vocab['Kanji']}"
                if 'Kana' in vocab and vocab['Kana']:
                    plain_text += f" ({vocab['Kana']})"
                plain_text += f" - {vocab['Meaning']}"

                visible_width = 0
                for char in plain_text:
                    if '\u4e00' <= char <= '\u9fff' or '\u3040' <= char <= '\u30ff':
                        visible_width += 2 
                    else:
                        visible_width += 1

                padding = max(2, column_width - visible_width)

                line_output += vocab_text + " " * padding
        print(line_output)

    input(f'\nPress Enter to return to the Main Menu... | ')


def display_characters():
    """
    Displays all characters for learning without quiz functionality.
    """
    all_characters = DATA.load_characters()
    
    if not all_characters:
        print(f"{UI.Colours.RED}No character data found!{UI.Colours.END}")
        return
    
    print(f"\n{UI.Colours.BOLD}{UI.Colours.BLUE}Learn the Characters{UI.Colours.END}")
    print(f"{UI.Colours.CYAN}Here are all the available characters and their pronunciations:{UI.Colours.END}\n")
    
    num_columns = 4
    char_per_column = (len(all_characters) + num_columns - 1) // num_columns
    column_width = 25

    for line in range(char_per_column):
        line_output = ''
        for col in range(num_columns):
            index = line + col * char_per_column
            if index < len(all_characters):
                char = all_characters[index]
                item_num = index + 1
                char_display = f'{item_num:2d}. {Colours.PURPLE}{char['Character']}{Colours.END} - {Colours.GREEN}{char['Correct Answer']}{Colours.END}'

                visible_length = len(f"{item_num:2d}. {char['Character']} - {char['Correct Answer']}")
                padding = column_width - visible_length

                line_output += char_display + ' ' * padding
        print(line_output)
    
    input(f"\nPress Enter to return to the Main Menu... | ")
    print()