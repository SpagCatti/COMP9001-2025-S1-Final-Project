"""
quiz_manager.py
Manages quiz elements and functionality for JapaneseStudy

References:
https://docs.python.org/3/library/random.html
https://docs.python.org/3/library/functions.html#ord
"""


import random
from typing import List, Dict, TypedDict, Tuple

import ui_handler as UI
import data_loader as DATA
import progress_manager as PROGRESS
import mistake_tracker as MISTAKE
import quiz_manager as QUIZ


class MistakeReview(TypedDict):
    """
    TypedDict for storing mistake information from quizzes.
    
    Fields:
        word: The primary text shown in the question 
              (Kanji for JLPT quiz, character for Character quiz)
        Kana: The secondary text for pronunciation 
              (Kana for JLPT quiz, empty for Character quiz)
        correct_answer: The correct meaning or reading that should have been chosen
        user_answer: The incorrect option that the user actually chose
    """
    word: str
    kana: str
    correct_answer: str
    user_answer: str


def generate_question(correct_content: Dict[str, str], all_content: List[Dict[str, str]], quiz_type: str) -> Tuple[str, List[str]]:
    """
    Generates a question based on the type. Options will include the correct answer and three other randomized wrong answers.

    Args:
        correct_item (dict[str, str]): A dictionary containing the correct vocab / character.
        all_content (list[dict[str, str]]): A list of dictionaries containing all vocabs / characters.
        quiz_type (str): A string representing the type of quiz to be displayed.

    Returns:
        tuple[str, list[str]]: A tuple with the question and a list of four answers (including one right and three wrong ones).
    """
    options = []
    correct_answer = ''
    question_prompt = ''
    option_type = ''

    # Display question in a format fitting for JLPT Quizzes
    if quiz_type == 'jlpt':
        kana = correct_content['Kana']
        kanji = correct_content['Kanji']
        question_prompt = f"{kana} ({kanji})"
        correct_answer = correct_content['Meaning']
        option_type = 'Meaning'
    
    # Display question in a format fitting for Character Quizzes
    elif quiz_type == 'character':
        question_prompt = correct_content ['Character']
        correct_answer = correct_content['Correct Answer']
        option_type = 'Correct Answer'
    
    # Add the correct answer to the option list
    options.append(correct_answer)

    # Make a list of other options as distractors
    wrong_options = []
    for content in all_content:
        if content[option_type] != correct_answer:
            wrong_options.append(content[option_type])

    # Shuffle the order of the wrong options and take the last three elements as distractors
    random.shuffle(wrong_options)
    options.extend(wrong_options[-3:])

    # Shuffle the order of the four options
    random.shuffle(options)

    return question_prompt, options


def get_correct_answer_index(options: List[str], correct_answer: str) -> int:
    """
    Gets the index (aka location) of the correct answer.

    Args:
        options (list[str]): A list of strings representing the options
        correct_answer (str): A string representing the correct option

    Returns:
        int: An integer value representing the index of the correct answer. (Must be 0-3)
    """
    return options.index(correct_answer)


def run_mistake_review(all_content: List[Dict[str, str]], quiz_type: str, mistakes_list: List[MistakeReview]) -> Tuple[int, List[MistakeReview]]:
    """
    Runs a quiz based on the mistakes the user had just made.
    
    Args:
        all_content (list[dict[str, str]]): A list of dictionaries containing all vocabs / characters.
        quiz_type (str): A string representing the type of quiz to be displayed.
        mistakes_list: List of dictionaries containing mistake information
    
    Returns:
        Tuple of:
            int: Number of mistakes cleared during this review
            List[MistakeReview]: List of remaining mistakes that weren't cleared
    """
    print(f"\n{UI.Colours.BOLD}{UI.Colours.YELLOW}Mistake Review{UI.Colours.END}")
    print(f"Let's review the {len(mistakes_list)} mistakes from this quiz.")
    print(f"For each question, try to answer correctly to clear it from your mistake list.")
    print()
    
    # Shuffle the order of the mistakes
    random.shuffle(mistakes_list)
    
    cleared_mistakes = 0
    remaining_mistakes = []
    user_quit_early = False
    
    q_no = 0
    while q_no < len(mistakes_list):
        mistake = mistakes_list[q_no]
        
        # Using the same method as generate_question
        if quiz_type == 'jlpt':
            question_prompt = mistake['word']
            correct_answer = mistake['correct_answer']
            option_type = 'Meaning'
        elif quiz_type == 'character':
            question_prompt = mistake['word']
            correct_answer = mistake['Correct Answer']
            option_type = 'Correct Answer'

        options = [correct_answer]
        
        # Make a list of other options as distractors
        wrong_options = []
        for content in all_content:
            if content[option_type] != correct_answer:
                wrong_options.append(content[option_type])
        
        # Shuffle the order of the wrong options and take the last three elements as distractors
        random.shuffle(wrong_options)
        options.extend(wrong_options[-3:])
        
        # Shuffle the order of the four options
        random.shuffle(options)
        
        # Print out the question
        print(f'{UI.Colours.BOLD}Review Q{q_no + 1}. Choose the meaning for:{UI.Colours.END}')
        print(f'{UI.Colours.BOLD}{UI.Colours.PURPLE}{question_prompt}{UI.Colours.END}' + 
              (f' ({mistake['kana']})' if mistake['kana'] != question_prompt else ''))
        
        # Print out the options
        for n, option in enumerate(options):
            option_letter = chr(65 + n)
            print(f'{UI.Colours.BOLD}{option_letter}{UI.Colours.END} | {option}')
        
        print()
        
        # Getting the user's choice
        user_choice = UI.get_user_choice('Answer | ', ['A', 'B', 'C', 'D', 'Q'])
        
        # The user chooses to quit
        if user_choice == 'Q':
            # Confirmation
            user_confirmation = UI.get_user_choice(f'{UI.Colours.YELLOW}Are you sure? You will lose all your current progress! [{UI.Colours.BOLD}Y/N{UI.Colours.END}{UI.Colours.YELLOW}] | {UI.Colours.END}', ['Y', 'N'])
            # Confirmed
            if user_confirmation == 'Y':
                # Add all remaining mistakes including the current one
                remaining_mistakes.extend(mistakes_list[q_no:])
                user_quit_early = True
                return cleared_mistakes, remaining_mistakes, user_quit_early
            # Cancelled
            elif user_confirmation == 'N':
                print(f'{UI.Colours.GREEN}Continuing review...{UI.Colours.END}\n')
                continue
        
        # Getting the indices of chosen option and correct option
        choice_index = ord(user_choice) - ord('A')
        correct_index = get_correct_answer_index(options, correct_answer)
        
        # Checking if the answer is correct
        if choice_index == correct_index:
            print(f'{UI.Colours.GREEN}Correct! This word will be removed from your mistakes.{UI.Colours.END}\n')
            cleared_mistakes += 1
        else:
            print(f'{UI.Colours.RED}Still incorrect.{UI.Colours.END}')
            print(f'{UI.Colours.YELLOW}Correct Answer: {chr(65 + correct_index)} | {correct_answer}.{UI.Colours.END}\n')
            # Keep this mistake in the list
            remaining_mistakes.append(mistake)

        q_no += 1
    
    # Show summary of review
    print(f"\n{UI.Colours.BOLD}Review Summary{UI.Colours.END}")
    print(f"You cleared {UI.Colours.GREEN}{cleared_mistakes}{UI.Colours.END}/{len(mistakes_list)} mistakes from your list.")
    
    return cleared_mistakes, remaining_mistakes, False


def run_mistake_practice():
    """
    Runs a practice session for mistakes the user has made previously.
    """
    # Load all mistakes from the database
    all_mistakes = MISTAKE.load_mistakes()
    
    if not all_mistakes or len(all_mistakes) == 0:
        print(f"\n{UI.Colours.YELLOW}There are no mistakes to practice right now.{UI.Colours.END}")
        print(f"Complete some quizzes first and come back later!")
        input(f"\nPress Enter to return to the Main Menu... | ")
        return
    
    # Load JLPT vocab for generating quiz options
    all_jlpt_vocab = []
    for level in ['N5', 'N4', 'N3', 'N2', 'N1']:
        all_jlpt_vocab.extend(DATA.load_jlpt_vocab(level))
    
    # Review mistakes
    corrected_mistake_num, remaining_mistakes, user_quit_early = QUIZ.run_mistake_review(all_jlpt_vocab, 'jlpt', all_mistakes)
    
    # If the user quit mid way, ignore any changes and do not modify the mistake database
    if user_quit_early:
        print(f'\n{UI.Colours.YELLOW}Quitting review. Mistakes made in previous quiz will still be saved.')

    else:
        MISTAKE.reset_mistakes()

        for mistake in remaining_mistakes:
            MISTAKE.add_mistake(
                mistake['word'],
                mistake['kana'],
                mistake['correct_answer'],
                mistake['user_answer']
            )
            
        print(f"\n{UI.Colours.GREEN}You cleared {corrected_mistake_num} out of {len(all_mistakes)} mistakes!{UI.Colours.END}")
        print(f"{UI.Colours.YELLOW}{len(remaining_mistakes)} mistakes remain in your practice list.{UI.Colours.END}")
    
    input(f"\nPress Enter to return to the Main Menu... | ")


def run_jlpt_quiz(level: str):
    """
    Runs a JLPT Quiz based on the specified level.

    Args:
        level (str): JLPT proficiency level (N5, N4, N3, N2, N1)
    """
    # Load all vocabs in this JLPT level into a list
    all_vocabs = DATA.load_jlpt_vocab(level)

    # Choose 10 random vocbularies
    quiz_content = random.sample(all_vocabs, 10)

    print(f'\n{UI.Colours.BLUE}You have chosen {UI.Colours.BOLD}{level}{UI.Colours.END}!\n')
    UI.display_quiz_tips()

    score = 0
    mistakes = []

    q_no = 0
    while q_no < len(quiz_content):
        content = quiz_content[q_no]
        question_prompt, options = generate_question(content, quiz_content, 'jlpt')

        # Print out the question
        print(f'{UI.Colours.BOLD}Q{q_no + 1}. Choose the meaning most suited for the following vocabulary.{UI.Colours.END}')
        print(f'{UI.Colours.BOLD}{UI.Colours.PURPLE}{question_prompt}{UI.Colours.END}')

        # Print out the options
        for n, option in enumerate(options):
            option_no = chr(65 + n)
            print(f'{UI.Colours.BOLD}{option_no}{UI.Colours.END} | {option}')

        print()

        # Getting the user's choice
        user_choice = UI.get_user_choice('Answer | ', ['A', 'B', 'C', 'D', 'Q'])

        # The user chooses to quit
        if user_choice == 'Q':
            # Confirmation
            user_confirmation = UI.get_user_choice(f'{UI.Colours.YELLOW}Are you sure? You will lose all your current progress! [{UI.Colours.BOLD}Y/N{UI.Colours.END}{UI.Colours.YELLOW}] | {UI.Colours.END}', ['Y', 'N'])
            # Confirmed
            if user_confirmation == 'Y':
                print(f'{UI.Colours.RED}Quiz terminated. No progress saved.{UI.Colours.END}\n')
                return
            # Cancelled
            elif user_confirmation == 'N':
                print(f'{UI.Colours.GREEN}Continuing quiz...{UI.Colours.END}\n')
                continue

        # Getting the indices of chosen option and correct option
        choice_index = ord(user_choice) - ord('A')
        correct_index = get_correct_answer_index(options, content['Meaning'])

        # Checking if the answer is right. Increment score if so.
        if choice_index == correct_index:
            print(f'{UI.Colours.GREEN}Correct.{UI.Colours.END}\n')
            score += 1

            kanji = content['Kanji']
            PROGRESS.add_mastered_vocab(level, kanji)
        else:
            print(f'{UI.Colours.RED}Wrong.{UI.Colours.END}')
            print(f'{UI.Colours.YELLOW}Correct Answer: {chr(65 + correct_index)} | {content['Meaning']}.{UI.Colours.END}\n')

            # Save this question into the mistake list
            mistakes.append({
                'word': content['Kanji'],
                'kana': content['Kana'],
                'correct_answer': content['Meaning'],
                'user_answer': options[choice_index]
            })

        q_no += 1

    # Present Quiz Summary
    print(f'Quiz Summary')
    print(f'You got {UI.Colours.GREEN}{score}{UI.Colours.END}/{len(quiz_content)} correct.\n')

    # If the user made mistakes in this attempt, show them for review
    if mistakes:
        print(f'{UI.Colours.BOLD}Review these words:{UI.Colours.END}')
        for mistake in mistakes:
            print(f'- {UI.Colours.PURPLE}{mistake['word']}{UI.Colours.END} (you chose: {UI.Colours.RED}{mistake['user_answer']}{UI.Colours.END}, correct: {UI.Colours.GREEN}{mistake['correct_answer']}{UI.Colours.END})')
        
        review_choice = UI.get_user_choice(f'\nWould you like to review these mistakes right now? [{UI.Colours.BOLD}Y/N{UI.Colours.END}] | ', ['Y', 'N'])

        if review_choice == 'Y':
            # Getting the number of corrected mistakes and the updated mistake list
            corrected_mistake_no, updated_mistakes, user_quit_early = run_mistake_review(all_vocabs, 'jlpt', mistakes)

            # If the user quit mid way, ignore any changes and do not modify the mistake database
            if user_quit_early:
                print(f'\n{UI.Colours.YELLOW}Quitting the review. Remaining mistakes will still be saved.')
                
                for mistake in mistakes:
                    MISTAKE.add_mistake(
                        mistake['word'],
                        mistake['kana'],
                        mistake['correct_answer'],
                        mistake['user_answer']
                    )
            else:
                if updated_mistakes:
                    print(f'You got {UI.Colours.GREEN}{corrected_mistake_no}{UI.Colours.END}/{len(mistakes)} correct.')
                    print(f'{UI.Colours.BOLD}Review these words again:{UI.Colours.END}')

                    for mistake in updated_mistakes:
                        print(f'- {UI.Colours.PURPLE}{mistake['word']}{UI.Colours.END} (you chose: {UI.Colours.RED}{mistake['user_answer']}{UI.Colours.END}, correct: {UI.Colours.GREEN}{mistake['correct_answer']}{UI.Colours.END})')

                        MISTAKE.add_mistake(
                            mistake['word'],
                            mistake['kana'],
                            mistake['correct_answer'],
                            mistake['user_answer']
                        )
                else:
                    print(f'{UI.Colours.GREEN}Great job! You cleared all your mistakes!{UI.Colours.END}')

        elif review_choice == 'N':
            print(f'{UI.Colours.BLUE}Good work! Your progress has been saved.\n{UI.Colours.END}')

            # Saving mistakes into the data bank
            for mistake in mistakes:
                MISTAKE.add_mistake(
                    mistake['word'],
                    mistake['kana'],
                    mistake['correct_answer'],
                    mistake['user_answer']
                )

    input(f'Press Enter to return to the Main Menu... | ')


def run_character_quiz():
    """
    Runs a Character Quiz to test knowledge of Japanese characters.
    """
    # Load all characters into a list
    all_characters = DATA.load_characters()

    # Choose 10 random characters
    quiz_content = random.sample(all_characters, 10)

    print(f'\n{UI.Colours.BLUE}You have chosen {UI.Colours.BOLD}Character Quiz{UI.Colours.END}!\n')
    UI.display_quiz_tips()

    score = 0

    q_no = 0
    while q_no < len(quiz_content):
        content = quiz_content[q_no]
        question_prompt, options = generate_question(content, quiz_content, 'character')

        # Print out the question
        print(f'{UI.Colours.BOLD}Q{q_no + 1}. Choose the reading most suited for the following character.{UI.Colours.END}')
        print(f'{UI.Colours.BOLD}{UI.Colours.PURPLE}{question_prompt}{UI.Colours.END}')

        # Print out the options
        for n, option in enumerate(options):
            option_no = chr(65 + n)
            print(f'{UI.Colours.BOLD}{option_no}{UI.Colours.END} | {option}')

        print()

        # Getting the user's choice
        user_choice = UI.get_user_choice('Answer | ', ['A', 'B', 'C', 'D', 'Q'])

        # The user chooses to quit
        if user_choice == 'Q':
            # Confirmation
            user_confirmation = UI.get_user_choice(f'{UI.Colours.YELLOW}Are you sure? You will lose all your current progress! [{UI.Colours.BOLD}Y/N{UI.Colours.END}{UI.Colours.YELLOW}] | {UI.Colours.END}', ['Y', 'N'])
            # Confirmed
            if user_confirmation == 'Y':
                print(f'{UI.Colours.RED}Quiz terminated. No progress saved.{UI.Colours.END}')
                return
            # Cancelled
            elif user_confirmation == 'N':
                print(f'{UI.Colours.GREEN}Continuing quiz...{UI.Colours.END}\n')
                continue

        # Getting the indices of chosen option and correct option
        choice_index = ord(user_choice) - ord('A')
        correct_index = get_correct_answer_index(options, content['Correct Answer'])

        # Checking if the answer is right. Increment score if so.
        if choice_index == correct_index:
            print(f'{UI.Colours.GREEN}Correct.{UI.Colours.END}\n')
            score += 1
        else:
            print(f'{UI.Colours.RED}Wrong.{UI.Colours.END}')
            print(f'{UI.Colours.YELLOW}Correct Answer: {chr(65 + correct_index)} | {content['Correct Answer']}.{UI.Colours.END}')
        
        # Move to the next question
        q_no += 1

    # Present Quiz Summary
    print(f'Quiz Summary')
    print(f'You got {UI.Colours.GREEN}{score}{UI.Colours.END}/{len(quiz_content)} correct.')

    # Simple evaluation
    if score == len(quiz_content):
        print(f'{UI.Colours.GREEN}Perfect score!{UI.Colours.END}')
    elif score >= len(quiz_content) * 0.6:
        print(f'{UI.Colours.GREEN}Great Job!{UI.Colours.END}')
    else:
        print(f'{UI.Colours.YELLOW}Keep cooking!{UI.Colours.END}\n')

    input(f'Press Enter to return to the Main Menu... | ')
