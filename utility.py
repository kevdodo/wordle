"""
TODO: Student name(s): Manuel Rodriguez and Kevin Do
TODO: Student email(s): mrodrig7@caltech.edu kdo@caltech.edu
TODO: Creating a database application and CLI for a user to play the
hangman-style game WORDLE in which users try to guess a word within a certain
number of attempts.

******************************************************************************
TODO:
- For full credit, remove any irrelevant comments, which are included in the
  template to help you get started. Replace this program overview with a
  brief overview of your application as well (including your name/partners name).
  This includes replacing everything in this *** section!
******************************************************************************
"""

import sys  # to print error messages to sys.stderr
import mysql.connector

# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Shows the user-friendly error messages
DEBUG = False


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn(user, password, host="localhost", port="3306", database="wordledb"):
    """ "
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            # Find port in MAMP or MySQL Workbench GUI or with
            # SHOW VARIABLES WHERE variable_name LIKE 'port';
            password=password,
            port=port,  # this may change and is viewable in XAMPP settings for MYSQL DB!
            database=database,  # replace this with your database name
        )
        print("Successfully connected.")
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr.write("Incorrect username or password when connecting to DB.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr.write("Database does not exist.")
        elif DEBUG:
            sys.stderr.write(str(err) + "\n")
        else:
            # A fine catchall client-facing message.
            sys.stderr.write("An error occurred, please contact the administrator.")
        sys.exit(1)


# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print("Good bye!")
    exit()
