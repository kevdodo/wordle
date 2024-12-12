"""
TODO: Student name(s): Manuel Rodriguez and Kevin Do
TODO: Student email(s): mrodrig7@caltech.edu kdo@caltech.edu
TODO: Creating a database application and CLI for a user to play the
hangman-style game WORDLE in which users try to guess a word within a certain
number of attempts.

******************************************************************************
Functions for logging in users, showing options, and quitting the program.

Admins can also see admin options, which are different from client options.
******************************************************************************
"""

import sys, os, mysql
import utility as util


DEBUG = True


# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def get_item_id(item_name):
    cursor = conn.cursor()
    sql = "SELECT item_id FROM shop WHERE item_name = %s;"
    try:
        cursor.execute(sql, (item_name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def get_player_id(username):
    cursor = conn.cursor()
    sql = "SELECT player_id FROM player_info WHERE username = %s;"
    try:
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def set_user_coins():
    os.system("clear")
    username = input("Enter the username: ")
    coins = input("Enter the number of coins: ")
    if not coins.isdigit():
        print("Invalid input. Please enter a number.")
        return

    cursor = conn.cursor()
    sql = "UPDATE player_info SET num_coins = %s WHERE username = %s;"
    try:
        cursor.execute(sql, (coins, username))
        conn.commit()
        print(f"{username} now has {coins} coins.")
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.stderr.write("Likely invalid username or coins.")


def remove_item():
    os.system("clear")
    username = input("Enter the username: ")
    item_name = input("Enter the item name: ")

    cursor = conn.cursor()
    sql = "DELETE FROM player_items NATURAL JOIN shop WHERE username = %s AND item_name = %s;"
    try:
        cursor.execute(sql, (username, item_name))
        conn.commit()
        print(f"{item_name} has been removed from {username}'s inventory.")
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def give_item():
    os.system("clear")
    username = input("Enter the username: ")
    item_name = input("Enter the item name: ")
    quantity = input("Enter the quantity: ")

    cursor = conn.cursor()
    sql = "INSERT INTO player_items (player_id, item_id, quantity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantity = %s"
    try:
        cursor.execute(
            sql, (get_player_id(username), get_item_id(item_name), quantity, quantity)
        )
        conn.commit()
        print(f"{item_name} has been added to {username}'s inventory.")

    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def delete_player():
    os.system("clear")
    username = input("Enter the username: ")

    cursor = conn.cursor()
    sql = "DELETE FROM player_info WHERE username = %s;"
    try:
        cursor.execute(sql, (username,))
        conn.commit()
        print(f"{username} has been deleted.")
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def show_all_players():
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT username FROM player_info;"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("All Players:")
        for row in rows:
            print(row["username"])
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def show_player_info():
    username = input("Enter the username: ")
    os.system("clear")
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT num_coins, item_name, quantity FROM player_info NATURAL JOIN player_items NATURAL JOIN shop WHERE player_id = %s"
    try:
        cursor.execute(sql, (get_player_id(username),))
        rows = cursor.fetchall()
        print("User Info:")
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def add_item():
    os.system("clear")
    item_name = input("Enter the item name: ")
    item_description = input("Enter the item description: ")
    item_cost = input("Enter the item cost: ")
    one_time_purchase = input("Is this item one-time use? (y): ")
    if one_time_use.lower() == "y":
        one_time_use = 1
    else:
        one_time_use = 0

    cursor = conn.cursor()
    sql = "INSERT INTO shop (item_name, item_description, item_cost, one_time_purchase) VALUES (%s, %s, %s, %s);"
    try:
        cursor.execute(sql, (item_name, item_description, item_cost, one_time_purchase))
        conn.commit()
        print(f"{item_name} has been added to the shop.")
    except mysql.connector.Error as err:
        sys.stderr.write(str(err))
        sys.exit(1)


def show_admin_options():
    os.system("clear")

    print("What would you like to do? ")
    print("1. Quit")
    print("2. Give player an item")
    print("3. Remove item from player")
    print("4. Set player coins")
    print("5. Show player info")
    print("6. Delete a player")
    print("7. Show all players")
    print("8. Add an item to the shop")
    print()

    ans = input("Enter an option: ").lower()
    match ans:
        case "1":
            util.quit_ui()
        case "2":
            give_item()
        case "3":
            remove_item()
        case "4":
            set_user_coins()
        case "5":
            show_player_info()
        case "6":
            delete_player()
        case "7":
            show_all_players()
        case "8":
            add_item()

    input("Press enter to continue...")
    show_admin_options()


if __name__ == "__main__":
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    os.system("clear")

    password = input("Enter the password for the admin user: ")
    conn = util.get_conn("wordleadmin", password, "localhost", 3306, "wordledb")
    show_admin_options()
