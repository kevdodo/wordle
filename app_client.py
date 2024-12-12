"""
Student name(s): Manuel Rodriguez and Kevin Do
Student email(s): mrodrig7@caltech.edu kdo@caltech.edu
Creating a database application and CLI for a user to play the
hangman-style game WORDLE in which users try to guess a word within a certain
number of attempts.

******************************************************************************
Functions for logging in users, showing options, and quitting the program.

Admins can also see admin options, which are different from client options.
******************************************************************************
"""

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
import sys  # to print error messages to sys.stderr
import mysql.connector  # to connect to the database

# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
import os  # to clear the screen
import random, re  # for generating random words and removing color from feedback
import time  # for sleep
from colorama import Fore, Style  # for colored text
from multiset import *  # for multiset operations
import utility as util


# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
def create_player(username, password, email, description):
    """
    Creates a new player in the database with the given username, password,
    email, and description.

    Args:
    username: string (maximum of 50 characters, cannot be empty)
    password: string (cannot be empty)
    email: string (maximum of 50 characters, cannot be empty)
    description: string (maximum of 200 characters, can be empty)

    Returns:
    TODO: 0 if the player was created successfully, and 1 otherwise.
    """
    cursor = _conn.cursor()
    query = "CALL sp_create_player(%s, %s, %s, %s)"
    try:
        cursor.execute(query, (username, password, email, description))
        _conn.commit()
        return 1
    except mysql.connector.Error as err:
        sys.stderr.write(
            str(err) + "\n"
        )  # should be a relatively descriptive SQL error
        return 0


def fetch_player(username, password):
    """
    Fetches a player's information from the database with the given username and password and
    assigns the value to a global variable, also shows player's items.

    Args:
    username: string (maximum of 50 characters, cannot be empty)
    password: string (cannot be empty)

    Returns:
        0 if the player is found, and 1 otherwise.
    """
    cursor = _conn.cursor(dictionary=True)
    # query should return the player username, email, description, created_at, and num_coins
    auth_query = "SELECT authenticate(%s, %s)"
    global _player_info

    try:
        cursor.execute(auth_query, (username, password))
        result = cursor.fetchone()

        if result[f"authenticate('{username}', '{password}')"]:
            cursor.callproc("get_player_info", (username,))
            for query_result in cursor.stored_results():
                result = query_result.fetchone()
                break
            _player_info = result
            _player_info["password"] = password
        else:
            return 0

        cursor.callproc("fetch_player_items", (_player_info["player_id"],))
        for query_result in cursor.stored_results():
            result = query_result.fetchall()
        _player_info["player_items"] = result

        return 1

    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def fetch_shop_items():
    """
    Fetches all items from the shop.

    Returns:
    A list of dictionaries, each containing the item_name, item_cost,
    item_description, and whether the item is a one time purchase.
    """
    cursor = _conn.cursor(dictionary=True)
    query = "SELECT * FROM shop"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def fetch_player_stats(username):
    """
    Fetches the player's stats from the database.

    Returns:
    A dictionary containing the player's username, email, description,
    created_at, and num_coins.
    """
    cursor = _conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_get_player_stats", (username,))
        for query_result in cursor.stored_results():
            result = query_result.fetchone()
            break
        return result
    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def player_has_item(item_name):
    """
    Checks if the player has the given item.

    Args:
    item_name: string

    Returns:
    True if the player has the item, and False otherwise.
    """
    for item in _player_info["player_items"]:
        if item["item_name"] == item_name:
            return True
    return False


def update_player_items(item, quantity):
    """
    Updates the player's items in the database.

    Args:
    item: information about the item to be updated
    quantity: the quantity of the item to be updated

    Returns:
    1 if the update was successful, and 0 otherwise.
    """
    global _player_info
    # if one_time_purchase and player_has_item(item_name): return 0
    if item["one_time_purchase"] and player_has_item(item["item_name"]):
        print("You already have this item.")
        time.sleep(2)
        return 0

    # if item is more expensive than user has coins, then can't buy it
    if item["item_cost"] * quantity > _player_info["num_coins"]:
        print("You don't have enough coins to buy this item.")
        time.sleep(2)
        return 0
    try:
        cursor = _conn.cursor()
        # TODO: query should call the procedure to update the players items and remove the cost from their coins
        cursor.callproc(
            "sp_use_buy_item", (_player_info["player_id"], item["item_id"], quantity)
        )
        _conn.commit()
        print("going to update player info after updating items")
        _player_info = fetch_player(_player_info["username"], _player_info["password"])
        print("Your Items have been updated successfully.")
        time.sleep(2)
        return 1

    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def print_player_items():
    """
    Prints the player's items.
    """
    print("_player_info['player_items']: ", _player_info["player_items"])
    if _player_info["player_items"]:
        print("You have the following items:")
        for item in _player_info["player_items"]:
            print(f"{item['item_name']}: {item['quantity']}")
    else:
        print("You have no items.")


def fetch_random_word():
    """
    Fetches a random word from the database.

    Returns:
    A random word from the database.
    """
    cursor = _conn.cursor()
    query = "CALL get_random_word()"
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result.get["get_random_word()"]
    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def fetch_random_fact():
    """
    Fetches a random fact from the database.

    Returns:
    A random fact from the database.
    """
    cursor = _conn.cursor()
    query = "SELECT get_random_fact()"
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result["get_random_fact()"]
    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def fetch_new_game(player_id, word):
    """
    Fetches a new game from the database.

    Args:
    player_id: int
    word: string

    Returns:
    The game_id of the new game.
    """
    cursor = _conn.cursor()
    query = "CALL sp_new_game(%s, %s)"  # should return the game_id
    try:
        cursor.execute(query, (player_id, word))
        _conn.commit()
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def new_guess_add(game_id, guess, attempts, guess_time):
    """
    Adds a new guess to the database.

    Args:
    game_id: int
    guess: string
    attempts: int
    guess_time: float
    """
    cursor = _conn.cursor()
    query = "CALL sp_add_guess(%s, %s, %s, %s)"  # no return
    try:
        cursor.execute(query, (game_id, guess, attempts, guess_time))
        _conn.commit()
    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def update_game_win(game_id, finished_time, attempts):
    """
    Updates the game board in the database when a player wins.

    Args:
    game_id: int
    finished_time: float
    attempts: int
    """
    cursor = _conn.cursor()
    # no return
    # updates score, player_stats (potentially with trigger), coins, games_played
    query = "CALL sp_game_won(%s, %s, %s)"

    try:
        cursor.execute(query, (game_id, finished_time, attempts))
        _conn.commit()
    except mysql.connector.Error as err:
        sys.stderr.write(str(err) + "\n")
        sys.exit(1)


def change_password():
    """
    Changes the player's password in the database.
    """
    os.system("clear")
    confirm = input("Are you sure you want to change your password? (y/n): ")
    while confirm != "y" and confirm != "n":
        confirm = input("Are you sure you want to change your password? (y/n): ")
    if confirm == "n":
        show_options()

    new_password = input("Enter your new password: ")
    confirm_password = input("Confirm your new password: ")
    if new_password != confirm_password:
        print("Passwords do not match.")
        time.sleep(2)
        change_password()

    cursor = _conn.cursor()
    try:
        cursor.callproc("sp_change_password", (_player_info["username"], new_password))
        _conn.commit()
        print("Password changed successfully.")
        time.sleep(2)
        show_options()
    except mysql.connector.Error as err:
        if err.sqlstate == "45000":
            sys.stderr.write(str(err) + "\n")
            print("Please try again.")
            time.sleep(2)
            change_password()
        else:
            sys.stderr.write(str(err) + "\n")
            sys.exit(1)


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)


def logged_in(username, password):
    """
    Logs in a user with the given username and password. This function
    should return the user's ID if the login was successful, and 0
    otherwise.
    """
    print()
    print("Logging in...")
    return fetch_player(username, password)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------


def main():
    """
    Main function for the command-line interface. This function should
    prompt the user for their username and password, and then allow them
    to play the game.
    """
    os.system("clear")
    print("Welcome to CS121's rendition of WORDLE!")
    ans = input("Do you have an account yet? (y/n):")
    while ans != "y" and ans != "n":
        os.system("clear")
        print("Welcome to CS121's rendition of WORDLE!")
        ans = input("Do you have an account yet? (y/n):")

    if ans == "n":
        print(
            "\nLet's get you set up. Please provide a username, password, email,"
            + "\nand description of yourself if you'd like!"
        )
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")
        description = input("Description (optional): ")
        if not create_player(username, password, email, description):
            print("There was an error creating your account. Please try again.")
            time.sleep(2)
            main()
        print("User created successfully.")
        time.sleep(1)
    else:
        print("Please enter your username and password to log in.")
        username = input("Username: ")
        password = input("Password: ")

    if not logged_in(username, password):
        print("There was an error logging you in. Please try again.")
        time.sleep(1)
        main()

    print(f'Welcome, {_player_info["username"]}!\n')
    print_player_items()

    print(
        "\nThough not necessary for functionality, the game will look better\n\
in full screen so please play in fullscreen to avoid visual aberations.\n"
    )
    print("Press (Enter) to continue...")
    input()
    os.system("clear")
    print(
        """
___  ___                                                _   _   __              _         
|  \/  |                                               | | | | / /             (_)        
| .  . |  __ _  _ __   _ __   _   _    __ _  _ __    __| | | |/ /   ___ __   __ _  _ __   
| |\/| | / _` || '_ \ | '_ \ | | | |  / _` || '_ \  / _` | |    \  / _ \ \ / /| || '_  \  
| |  | || (_| || | | || | | || |_| | | (_| || | | || (_| | | |\  \|  __/ \ V / | || | | | 
\_|  |_/ \__,_||_| |_||_| |_| \__, |  \__,_||_| |_| \__,_| \_| \_/ \___|  \_/  |_||_| |_| 
                               __/ |                                                      
                              |___/                                                       
                                      _                
                                     | |   _ 
 _ __   _ __  ___  ___   ___  _ __   | |_ (_)
| '_ \ | '__|/ _ \/ __| / _ \| '_ \  | __|
| |_) || |  |  __/\__ \|  __/| | | | | |_  _
| .__/ |_|   \___||___/ \___||_| | |  \__|(_)
| |
|_|
          """
    )
    time.sleep(3)
    show_options()


def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    os.system("clear")

    if player_has_item("HIDDEN 1"):
        print(
            Fore.LIGHTGREEN_EX
            + """
 __ __ __       ______       ______        ______       __           ______      
/_//_//_/\     /_____/\     /_____/\      /_____/\     /_/\         /_____/\     
\:\:\:\ \ \    \:::_ \ \    \:::_ \ \     \:::_ \ \    \:\ \        \::::_\/_    
 \:\:\:\ \ \    \:\ \ \ \    \:(_) ) )_    \:\ \ \ \    \:\ \        \:\/___/\   
  \:\:\:\ \ \    \:\ \ \ \    \: __ `\ \    \:\ \ \ \    \:\ \____    \::___\/_  
   \:\:\:\ \ \    \:\_\ \ \    \ \ `\ \ \    \:\/.:| |    \:\/___/\    \:\____/\ 
    \_______\/     \_____\/     \_\/ \_\/     \_____/      \_____\/     \_____\/ 
"""
            + Style.RESET_ALL
        )
    if player_has_item("HIDDEN 2"):
        print("Did you know...\n")
        print(fetch_random_fact())
        print()

    print("What would you like to do? ")
    if not (player_has_item("HIDDEN 2") and player_has_item("HIDDEN 1")):
        print(
            """  Hmm.. looks bland no? Seems like there\'s something missing...
               perhaps you could add something from the shop?"""
        )
        print()

    print("  (p) - Play a game! By default you have 5 attempts to guess the word.")
    print("  (s) - Open the shop! Spend your coins on items to help you in the game.")
    print("  (i) - View your current items (also viewable in the shop).")
    print("  (m) - See your stats!")
    print("  (o) - See your friends' stats if you know their usernames!")
    print("  (c) - Change your password.")
    print("  (q) - quit")
    print()
    ans = input("Enter an option: ")
    match ans:
        case "q":
            util.quit_ui()
        case "p":
            start_game()
        case "s":
            start_shop()
        case "i":
            show_items()
        case "m":
            show_player_stats(_player_info["username"])  # TODO
        case "o":
            show_player_stats(
                input("Enter the username of the player you'd like to see: ")
            )
        case "c":
            change_password()
        case _:
            show_options()


def play_wordle(word, hard_mode=False, max_attempts=5):
    def get_item():
        """
        Allows the user to use items in the game.

        Returns:
        The name of the item the user used.
        """
        os.system("clear")
        # print the items that the user has according to the _player_info global
        # variable
        print_player_items()

        # prompt the user to use an item
        item_name = input(
            "Enter the name of the item you'd like to use (must match exactly), or press (b) to return to the game: "
        )
        # should be of length 1 since "item_name" is unique in database
        item = [
            item
            for item in _player_info["player_items"]
            if item["item_name"] == item_name
        ]
        if item_name == "b":
            return None
        elif len(item) == 0:
            print("You don't have that item.")
            return None
        elif item[0]["one_time_purchase"]:
            print("You can't use that item here!")
            return None
        else:
            update_player_items(item[0], -1)
            return item[0]["item_name"]

    def remove_color(letter):
        """
        Removes color from the feedback and makes it lowercase to
        make it easier to compare to the user's guess.
        """
        return re.sub(r"_|\033\[\d+m", "", letter).lower()

    def print_feedbacks():
        """
        Prints the user's guesses.
        """
        for f in feedbacks:
            print(" ".join(f))
        if not won and attempts < max_attempts:
            print(" ".join(["_" for _ in word]))
        else:
            print()

    os.system("clear")
    won = False
    start_time = time.time()
    word = word.lower()
    wrong_letters = set()
    guesses = set()
    feedbacks = []
    prev_feedback = ["_" for _ in word]
    attempts = 0
    items_used = 0
    time_freeze = False
    tot_guess_time = 0
    invalid = False
    game_id = None
    while attempts < max_attempts:
        os.system("clear")
        print(f"You have {max_attempts - attempts} attempts left.")

        if not hard_mode:
            prev_feedback = ["_" for _ in word]  # for normal mode
        print_feedbacks()
        print()
        print(
            Fore.BLUE + f"Wrong letters: {', '.join(wrong_letters)}" + Style.RESET_ALL
        )
        print(Fore.BLUE + f"Guesses: {', '.join(guesses)}" + Style.RESET_ALL)
        if attempts > 0:
            print(Fore.BLUE + f"Time taken: {guess_time:.2f} seconds" + Style.RESET_ALL)

        guess = input("\nEnter your guess, see your items (i), or quit (q): ")

        # continue and break work as if match keyword were not there
        match guess:
            case "i":
                new_item = get_item()
                match new_item:
                    case "Extra Guess":
                        max_attempts += 1
                    case "Freeze Time":
                        time_freeze = True
                    case "Hint":
                        missing_letters = set.difference(set(word), guesses)
                        if missing_letters:
                            hint = random.choice(
                                tuple(set.difference(set(word), guesses))
                            )
                            print(
                                f"A letter in the word that you're missing is {Fore.GREEN + hint + Style.RESET_ALL}."
                            )
                        else:
                            print(
                                "You've already guessed all the right letters! You've got this!"
                            )
                        input("Press enter to continue.")
                continue
            case "q":
                break

        if guess in guesses:
            print(Fore.YELLOW + "You've already guessed that word." + Style.RESET_ALL)
            time.sleep(1)
            continue
        if len(guess) != len(word):
            print(
                Fore.YELLOW
                + "Please enter a word of the same length."
                + Style.RESET_ALL
            )
            time.sleep(1)
            continue

        if hard_mode:
            best_guess = Multiset(
                "".join([remove_color(l) for l in prev_feedback])
            )  # get the best guess from the previous feedback
            # check if best guess is a subset of the current guess
            if not best_guess.issubset(Multiset(guess)):
                print(
                    Fore.RED
                    + "Invalid guess. Must use all letters from previous guesses."
                    + Style.RESET_ALL
                )
                time.sleep(1)
                continue

        letters_left = Multiset(word)
        if attempts == 0:
            game_id = fetch_new_game(
                _player_info["player_id"], word
            )  # returns the game_id

        if time_freeze:
            guess_time = 0
            time_freeze = False
        else:
            guess_time = time.time() - start_time

        tot_guess_time += guess_time
        start_time = time.time()
        new_guess_add(game_id, guess, attempts, guess_time)

        new_feedback = ["_" for _ in word]
        for i, letter in enumerate(guess):
            if hard_mode:
                # checks that if a letter was placed correct previously, the new guess
                # has it in the same position
                if (
                    prev_feedback[i].startswith(Fore.GREEN)
                    and remove_color(prev_feedback[i]) != letter
                ):
                    print("prev: ", repr(prev_feedback[i]))
                    print("letter: ", repr(letter))
                    print(
                        Fore.RED
                        + "Invalid guess for hard mode. Must use all letters from previous guesses."
                        + Style.RESET_ALL
                    )
                    time.sleep(5)
                    invalid = True
                    break

            if letter == word[i]:
                new_feedback[i] = Fore.GREEN + letter.upper() + Style.RESET_ALL
                letters_left[letter] -= 1

        # Need to stop comparing if the guess was invalid
        if invalid:
            invalid = False
            continue

        # need to do two loops because don't know ahead of time how many letters
        # are placed correctly from the guess
        for i, letter in enumerate(guess):
            if letters_left[letter] > 0:
                new_feedback[i] = Fore.YELLOW + letter.upper() + Style.RESET_ALL
                letters_left[letter] -= 1
            elif letter not in word:
                wrong_letters |= set(letter)

        feedbacks.append(new_feedback)
        prev_feedback = new_feedback
        guesses.add(guess)
        attempts += 1

        if guess == word:
            won = True
            # guess time in seconds
            update_game_win(game_id, tot_guess_time, attempts)
            break

    os.system("clear")
    print_feedbacks()

    return (won, attempts, word, tot_guess_time)


def start_game(max_attempts=5):
    """
    Starts the game for the user.
    """
    os.system("clear")
    print("Welcome to WORDLE!")
    print(
        f"You have {max_attempts} total attempts to guess the word (unless you use your items!)"
    )
    print(
        "You can also play with hard mode on, which requires you to use all the letters from previous guesses."
    )

    hard_mode = input("\nWould you like to play in hard mode? (y/n): ")
    while hard_mode != "y" and hard_mode != "n":
        hard_mode = input("Would you like to play in hard mode? (y/n): ")

    if hard_mode == "y":
        print("\nYou've chosen to play in hard mode for this game!")
        hard_mode = True
    else:
        print("\nYou've chosen to play in normal mode for this game!")
        hard_mode = False
    print("Good luck!")
    time.sleep(2)

    word = fetch_random_word()
    won, attempts, word, tot_guess_time = play_wordle(word, hard_mode, max_attempts)
    if won:
        print(
            Fore.GREEN
            + f"You won! You guessed the word with {attempts} attempts in {tot_guess_time:.2f} seconds."
            + Style.RESET_ALL
        )
        # would have triggers to update player stats and coins based on their
        # score this game
    else:
        print(
            Fore.RED + f"You"
            "ve reached the maximum number of attempts or chosen to leave the game :("
        )
        print("The word was " + Fore.GREEN + f"{word.upper()}." + Style.RESET_ALL)

    ans = input("would you like to play again? (y/n):")
    if ans == "y":
        start_game()
    else:
        show_options()


def start_shop():
    """
    Opens the shop for the user.
    """
    os.system("clear")
    print("Welcome to the shop! Here you can buy items to help you in the game.")
    print_player_items()
    print("\nHere are the items available for purchase:")

    for idx, item in enumerate(_shop_items):
        print(f"[{idx + 1}] {item['item_name']} ---- {item['item_cost']} coins")
        print(f"    *{item['item_description']}")
        if item["one_time_purchase"]:
            print("    *One time effect only (but you can flex by buying more = D ).")

    print(f'\nYou have {_player_info["num_coins"]} coins.')

    ans = input(
        "Enter the number of the item you would like to purchase, or press (b) to go back to the main menu: "
    )
    if int(ans) in range(1, len(_shop_items) + 1):
        update_player_items(_shop_items[int(ans) - 1], 1)
        start_shop()
    if ans == "b":
        show_options()
    else:
        start_shop()


def show_items():
    """
    Displays the user's purchased items and stats.
    """
    os.system("clear")
    print_player_items()
    print(f'\nYou have {_player_info["num_coins"]} coins.')

    print("\nPress b to go back to the main menu.\n")
    ans = input("Enter an option: ")
    while ans != "b":
        if ans == "":
            pass
        ans = input("Enter an option: ")
    show_options()


def show_player_stats(username):
    """
    Displays the stats of the given player.
    """
    os.system("clear")
    print(f"Stats for {username}:\n")
    stats = fetch_player_stats(username)
    if not stats:
        print(
            "Looks like this user either doesn't have an account or they haven't played a game yet!"
        )
        print("You need to play a game before you can see your stats.")
    else:
        for k, v in stats.items():
            print(f"{k}: {v}")

    ans = input("\nPress b to go back to the main menu.")
    while ans != "b":
        if ans == "":
            pass
        ans = input("Enter an option: ")
    show_options()


if __name__ == "__main__":
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    os.system("clear")

    _conn = util.get_conn("wordleclient", "")
    _player_info = {}
    _shop_items = fetch_shop_items()
    main()
    _conn.close()
