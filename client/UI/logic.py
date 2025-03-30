# hangman_logic.py
import random
import os

MAX_ERRORS = 6

class HangmanGame:
    def __init__(self, word_list, max_attempts=MAX_ERRORS):
        self.word_list = word_list
        self.secret_word = random.choice(word_list).lower()
        self.guessed = ["_" for _ in self.secret_word]
        self.max_attempts = max_attempts
        self.attempts_left = max_attempts
        self.wrong_letters = []
        self.game_over = False
        self.message = ""
        self.points = 0

    def guess_letter(self, letter):
        letter = letter.lower()
        if self.game_over:
            return

        # Validate that a single alphabetical letter is entered
        if not letter.isalpha() or len(letter) != 1:
            self.message = "Please enter a valid letter."
            return

        # Check if the letter has already been used
        if letter in self.guessed or letter in self.wrong_letters:
            self.message = "You already tried that letter."
            return

        # Process the guess
        letter_found = False
        for i, char in enumerate(self.secret_word):
            if char == letter:
                if self.guessed[i] == "_":  # Only update if not already revealed
                    self.guessed[i] = letter
                    if not letter_found:
                        self.points += 20  # Add points once per letter
                        letter_found = True

        if not letter_found:
            self.points -= 10
            self.attempts_left -= 1
            self.wrong_letters.append(letter)
            self.message = "Incorrect letter."
        else:
            self.message = "Good!"

        # Check win or lose conditions
        if "_" not in self.guessed:
            self.message = "Congratulations, you won!"
            self.game_over = True
        if self.attempts_left <= 0:
            self.message = f"You lost. The word was '{self.secret_word}'."
            self.guessed = list(self.secret_word)
            self.game_over = True

    def get_display_word(self):
        return " ".join(self.guessed)

    def get_wrong_letters(self):
        return ", ".join(self.wrong_letters)

def get_word_list(filename="words.txt"):
    """Returns a list of words from the file.
       If the file doesn't exist or is empty, returns ['default'].
    """
    if not os.path.exists(filename):
        return ["default"]
    with open(filename, "r") as f:
        words = [line.strip() for line in f if line.strip()]
    if not words:
        words = ["default"]
    return words

def add_word_to_file(new_word, filename="words.txt"):
    """Adds the new word to the file if it doesn't already exist.
       Returns (True, message) if added, or (False, message) on error.
    """
    new_word = new_word.lower().strip()
    if not new_word.isalpha():
        return False, "The word must contain only letters."
    words = get_word_list(filename)
    if new_word in words:
        return False, f"The word '{new_word}' already exists."
    with open(filename, "a") as f:
        f.write(new_word + "\n")
    return True, f"Word '{new_word}' added successfully."
