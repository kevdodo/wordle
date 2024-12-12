import os
import time

# for i in range(10):
#     os.system('clear')  # Clears the console
#     print(f'New output: {i}')  # Prints the new output
#     time.sleep(1)  # Waits for 1 second before the next update

from colorama import Fore, Style
from multiset import *

def play_wordle(word, max_attempts=5):
    # letters_left = Multiset(word)
    word = word.lower()
    wrong_letters = []
    feedback = ['_' for _ in word]
    attempts = 0
    while attempts < max_attempts:
        guess = input("Enter your guess: ").lower()
        if len(guess) != len(word):
            print("Please enter a word of the same length.")
            continue
        for (i, letter) in enumerate(guess):
            if feedback[i] != '_':
                continue
            if letter == word[i]:
                feedback[i] = Fore.GREEN + letter.upper() + Style.RESET_ALL
            elif letter in word:
                feedback[i] = Fore.YELLOW + letter.upper() + Style.RESET_ALL
            else:
                wrong_letters.append(letter)
        print(' '.join(feedback))
        print(Fore.RED + f"Wrong letters: {', '.join(wrong_letters)}" + Style.RESET_ALL)
        if guess == word:
            print(Fore.GREEN + "Congratulations, you've guessed the word!" + Style.RESET_ALL)
            break
        attempts += 1
    if attempts == max_attempts:
        print(Fore.RED + f"You've reached the maximum number of attempts. The word was {word}." + Style.RESET_ALL)

os.system('clear')
play_wordle('apple')  # Example usage