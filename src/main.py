"""
main.py
Manages most of the logic in JapaneseStudy.
"""


import ui_handler as UI
import data_loader as DATA
import quiz_manager as QUIZ
import mistake_tracker as MISTAKE
import progress_manager as PROGRESS


def main():
    """
    Main function that runs the JapaneseStudy application.
    """
    UI.display_title("JapaneseStudy")

    while True:
        mistake_count = MISTAKE.get_mistake_count()
        choice = UI.display_main_menu(mistake_count)

        # JLPT Quiz
        if choice == '1':
            user_progress = PROGRESS.load_user_progress()
            level_choice = UI.display_jlpt_quiz_menu(user_progress)

            level_map = {
                '1': 'N5',
                '2': 'N4', 
                '3': 'N3',
                '4': 'N2',
                '5': 'N1',
                'R': 'Return'
            }

            if level_choice in level_map and level_map[level_choice] != 'Return':
                level = level_map[level_choice]
                QUIZ.run_jlpt_quiz(level)
            else:
                continue
        
        # Character Quiz
        elif choice == '2':
            QUIZ.run_character_quiz()
        
        # Learn the Vocabs
        elif choice == '3':
            level = UI.display_jlpt_vocab_menu()
            if level != 'return':
                UI.display_vocabulary(level)
            else:
                print()

        # Learn the Characters
        elif choice == '4':
            UI.display_characters()

        # Mistake Practice
        elif choice == '5':
            QUIZ.run_mistake_practice()

        # Reset
        elif choice == '6':
            confirmation = UI.get_user_choice(f'{UI.Colours.RED}WARNING: THIS WILL SET ALL YOUR DATA INCLUDING PROGRESS AND MISTAKES\n'
                                              f'This cannot be undone. Are you sure? [{UI.Colours.BOLD}Y/N{UI.Colours.END}{UI.Colours.RED}] | {UI.Colours.END}', 
                                              ['Y', 'N'])
            
            if confirmation == 'Y':
                progress_reset = PROGRESS.reset_progress()
                mistake_reset = MISTAKE.reset_mistakes()

                if progress_reset and mistake_reset:
                    print(f'{UI.Colours.GREEN}All data has been reset successfully.{UI.Colours.END}\n')
                else:
                    print(f'{UI.Colours.RED}There are an issue resetting some data. Please check the files.{UI.Colours.END}')
            else:
                print(f'{UI.Colours.GREEN}Reset cancelled.{UI.Colours.END}')
        
        # Quitting the application
        elif choice == '7':
            confirmation = UI.get_user_choice(f'{UI.Colours.RED}Are you sure you want to quit? [{UI.Colours.BOLD}Y/N{UI.Colours.END}{UI.Colours.RED}] | {UI.Colours.END}', 
                                              ['Y', 'N'])
            
            if confirmation == 'Y':
                print(f"\n{UI.Colours.GREEN}Thanks for using JapaneseStudy! See you next time! 頑張りましょう！{UI.Colours.END}")
                break
            else:
                print(f"{UI.Colours.GREEN}Continuing...{UI.Colours.END}\n")
                continue


if __name__ == "__main__":
    main()
    