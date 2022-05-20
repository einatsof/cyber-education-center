import os
import os.path


MAX_TRIES = 6
HANGMAN_ASCII_ART = r"""

   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                       |___/"""
HANGMAN_PHOTOS = {
    0: """\033[33mx-------x\033[00m




    """,
    1: """\033[33mx-------x
|
|
|
|
|\033[00m""",
    2: """\033[33mx-------x
|       |
|\033[00m       0\033[33m
|
|
|\033[00m""",
    3: """\033[33mx-------x
|       |
|       \033[00m0\033[33m
|       \033[35m|\033[33m
|
|\033[00m""",
    4: """\033[33mx-------x
|       |
|       \033[00m0\033[33m
|      \033[35m/|\\\033[33m
|
|\033[00m""",
    5: """\033[33mx-------x
|       |
|       \033[00m0\033[33m
|      \033[35m/|\\\033[33m
|      \033[36m/\033[33m
|\033[00m""",
    6: """\033[33mx-------x
|       |
|       \033[00m0\033[33m
|      \033[35m/|\\\033[33m
|      \033[36m/ \\\033[33m
|\033[00m"""
    }
WIN_ASCII_ART = r"""
███████████████████████
█▄─█▀▀▀█─▄█▄─▄█▄─▀█▄─▄█
██─█─█─█─███─███─█▄▀─██
▀▀▄▄▄▀▄▄▄▀▀▄▄▄▀▄▄▄▀▀▄▄▀
"""
LOSE_ASCII_ART = r"""
████████████████████████
█▄─▄███─▄▄─█─▄▄▄▄█▄─▄▄─█
██─██▀█─██─█▄▄▄▄─██─▄█▀█
▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀
"""


def print_logo():
    """Clear screen and print the game logo in green.
    :return: None
    """
    cls()
    print_green(HANGMAN_ASCII_ART + "\n" + str(MAX_TRIES))


def check_win(secret_word, old_letters_guessed):
    """Check if player guessed all letters of the secret word and won.
    :param secret_word: the secret word
    :param old_letters_guessed: all letters player guessed so far
    :type secret_word: str
    :type old_letters_guessed: list
    :return: True if player won and False if not
    :rtype: bool
    """
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


def show_hidden_word(secret_word, old_letters_guessed):
    """Show the letters of the secret word that were already guessed
       and blanks for not yet guessed letters.
    :param secret_word: the secret word
    :param old_letters_guessed: all letters player guessed so far
    :type secret_word: str
    :type old_letters_guessed: list
    :return: string with letters and blanks
    :rtype: str
    """
    progress_str = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            progress_str += letter + " "
        else:
            progress_str += "_ "
    return progress_str


def check_valid_input(letter_guessed, old_letters_guessed):
    """Checks if the input is a single character of the English alphabet
       or not, and if the character was already guessed before.
    :param letter_guessed: input string from user
    :param old_letters_guessed: a list of all valid characters guessed so far
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: True if letter_guessed is a valid input
             that was not guessed before and False otherwise
    :rtype: bool
    """
    if len(letter_guessed) != 1:
        return False
    elif len(letter_guessed) == 1 and not letter_guessed.isalpha():
        return False
    elif letter_guessed.lower() in old_letters_guessed:
        return False
    else:
        return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """Updates the list of letters that have been guessed or prints
       a message if the letter already exist on the list.
    :param letter_guessed: input string from user
    :param old_letters_guessed: list of valid letter already been guessed
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: if letter is valid and new return True else return False
    :rtype: bool
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print("X\n" + " -> ".join(sorted(old_letters_guessed)))
        print_red("Try again")
        return False


def choose_word(file_path, index):
    """Choose a secret word from a file according to user index input.
    :param file_path: path to a file with words
    :param index: user input number
    :type file_path: str
    :type index: int
    :return: the word at index "index"
    :rtype: str
    """
    index -= 1
    all_words = []
    file_obj = open(file_path, "r")
    all_words = file_obj.read().split()
    if index >= len(all_words):
        # loop index if too big
        index = index % len(all_words)
    return all_words[index]


def cls():
    """Clears the screen.
    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def print_letters_box(old_letters_guessed):
    """Print a box with all ABC letters and an indication
       which letters already been guessed.
    :param old_letters_guessed: list of valid letter already been guessed
    :type old_letters_guessed: list
    :return: None
    """
    letters_string = ""
    list_of_letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    for letter in list_of_letters:
        if letter in old_letters_guessed:
            letters_string += "\033[90m" + letter + "\033[00m "
        else:
            letters_string += letter + " "
    print("┌─────────────────────────────────────────────────────┐")
    print("│ " + letters_string + "│")
    print("└─────────────────────────────────────────────────────┘")


def print_game_screen(num_of_tries, secret_word, old_letters_guessed):
    """Prints the game screen
    :return: None
    """
    print(HANGMAN_PHOTOS[num_of_tries], "\n")
    print(show_hidden_word(secret_word, old_letters_guessed))
    print_letters_box(old_letters_guessed)


def print_red(str):
    """Print a string to console in red using ANSI escape code.
    :param str: a string
    :type str: str
    :return: None
    """
    print("\033[91m{}\033[00m" .format(str))


def print_gold(str):
    """Print a string to console in gold using ANSI escape code.
    :param str: a string
    :type str: str
    :return: None
    """
    print("\033[93m{}\033[00m" .format(str))


def print_green(str):
    """Print a string to console in green using ANSI escape code.
    :param str: a string
    :type str: str
    :return: None
    """
    print("\033[32m{}\033[00m" .format(str))


def get_file_path():
    """Checks validity of file path.
    :return: valid path to file
    :rtype: str
    """
    user_input = input("Enter file path: ")
    if os.path.isfile(user_input):
        return user_input
    else:
        print("File not found. Please try again.")
        return get_file_path()


def get_index():
    """Checks validity of index from user.
    :return: valid index
    :rtype: int
    """
    user_input = input("Enter index: ")
    if user_input.isdigit() and int(user_input) > 0:
        return int(user_input)
    else:
        print("Input is not valid.")
        return get_index()


def game():
    """Play the hangman game.
    :return: None
    """
    secret_word = ""
    old_letters_guessed = []
    num_of_tries = 0
    print_logo()
    # get data from user
    file_path = get_file_path()
    index = get_index()
    secret_word = choose_word(file_path, index)
    # start the game
    print_logo()
    print("Let’s start!")
    print_game_screen(num_of_tries, secret_word, old_letters_guessed)
    while(num_of_tries < MAX_TRIES):
        # get guessed letter from user
        user_input = input("\nGuess a letter: ").lower()
        # check letter
        if try_update_letter_guessed(user_input, old_letters_guessed):
            print_logo()
            if user_input not in secret_word:
                num_of_tries += 1
                print_red(":(")
            else:
                print("")
            print_game_screen(num_of_tries, secret_word, old_letters_guessed)
            # check if user won
            if check_win(secret_word, old_letters_guessed):
                print_gold(WIN_ASCII_ART)
                break
    # in case user lost
    if num_of_tries == MAX_TRIES:
        print_red(LOSE_ASCII_ART)


def play_again():
    """Check if the user wants to play again.
    :return: True if yes and False if no
    :rtype: bool
    """
    user_input = input("Play again? y/n: ")
    if user_input == "y":
        return True
    elif user_input == "n":
        return False
    else:
        return play_again()


def main():
    play = True
    while(play):
        game()
        play = play_again()

if __name__ == "__main__":
    main()
