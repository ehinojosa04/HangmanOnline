# main.py
import tkinter as tk
from tkinter import ttk
from logic import HangmanGame, get_word_list, add_word_to_file

def start_game():
    game_win = tk.Toplevel(root)
    game_win.title("Hangman Game Online")
    game_win.geometry("600x400")
    game_win.configure(bg="#ffffff")

    words = get_word_list()
    game = HangmanGame(words)

    word_var = tk.StringVar(value=game.get_display_word())
    attempts_var = tk.StringVar(value=f"Attempts left: {game.attempts_left}")
    wrong_var = tk.StringVar(value="Wrong letters:")
    points_var = tk.StringVar(value=f"Points: {game.points}")
    message_var = tk.StringVar(value="")

    tk.Label(game_win, textvariable=word_var, font=("Helvetica", 24), bg="#ffffff").pack(pady=20)
    tk.Label(game_win, textvariable=attempts_var, font=("Helvetica", 14), bg="#ffffff").pack(pady=5)
    tk.Label(game_win, textvariable=wrong_var, font=("Helvetica", 14), bg="#ffffff").pack(pady=5)
    tk.Label(game_win, textvariable=points_var, font=("Helvetica", 14), bg="#ffffff").pack(pady=5)
    tk.Label(game_win, textvariable=message_var, font=("Helvetica", 16), bg="#ffffff", fg="red").pack(pady=10)

    letter_entry = tk.Entry(game_win, font=("Helvetica", 16))
    letter_entry.pack(pady=10)
    letter_entry.focus_set()

    def on_guess():
        letter = letter_entry.get()
        letter_entry.delete(0, tk.END)
        game.guess_letter(letter)
        word_var.set(game.get_display_word())
        attempts_var.set(f"Attempts left: {game.attempts_left}")
        wrong_var.set("Wrong letters: " + game.get_wrong_letters())
        points_var.set(f"Points: {game.points}")
        message_var.set(game.message)
        if game.game_over:
            letter_entry.config(state="disabled")

    ttk.Button(game_win, text="Guess", command=on_guess).pack(pady=10)
    ttk.Button(game_win, text="Close Game", command=game_win.destroy).pack(pady=10)

def add_words_ui():
    add_win = tk.Toplevel(root)
    add_win.title("Add Words")
    add_win.geometry("500x400")
    add_win.configure(bg="#f0f0f0")

    current_words = get_word_list()
    words_str = "\n".join(current_words)
    tk.Label(add_win, text="Current Words:", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=10)
    words_label = tk.Label(add_win, text=words_str, font=("Helvetica", 12), bg="#f0f0f0", justify="left")
    words_label.pack(pady=5, padx=10)

    tk.Label(add_win, text="New Word:", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=10)
    new_word_entry = tk.Entry(add_win, font=("Helvetica", 14))
    new_word_entry.pack(pady=5)

    status_var = tk.StringVar(value="")
    status_label = tk.Label(add_win, textvariable=status_var, font=("Helvetica", 12), fg="blue", bg="#f0f0f0")
    status_label.pack(pady=5)

    def on_add():
        new_word = new_word_entry.get().strip()
        new_word_entry.delete(0, tk.END)
        success, msg = add_word_to_file(new_word)
        status_var.set(msg)
        if success:
            updated_words = get_word_list()
            words_label.config(text="\n".join(updated_words))

    ttk.Button(add_win, text="Add", command=on_add).pack(pady=10)
    ttk.Button(add_win, text="Close", command=add_win.destroy).pack(pady=10)

def show_about(master):
    """Displays the 'About' window with project information."""
    about_win = tk.Toplevel(master)
    about_win.title("About")
    about_win.geometry("655x555")
    about_win.configure(bg="#f0f0f0")

    tk.Label(about_win, text="About the Application", 
             font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    team_info = (
        "Team Members:\n"
        " - Emiliano Hinojosa Guzmán (0252496)\n"
        " - Diego Amin Hernández Pallares (0250146)\n"
        " - Mario Alejandro Rodriguez Gonzalez (0235810)\n\n"
        "Subject: Distributed Computing\n"
        "Professor: Dr. Juan Carlos López Pimentel\n"
        "Date: 01/04/2025\n"
    )
    tk.Label(about_win, text=team_info, font=("Helvetica", 12),
             justify="left", bg="#f0f0f0").pack(pady=10, padx=10)

    game_info = (
        "How to Play:\n\n"
        "The objective is to guess the hidden word letter by letter.\n"
        "You have 6 attempts. Each correct letter adds 20 points and each mistake subtracts 10 points.\n"
        "You win if you guess the word before running out of attempts; otherwise, you lose.\n"
    )
    tk.Label(about_win, text=game_info, font=("Helvetica", 12),
             justify="left", bg="#f0f0f0").pack(pady=10, padx=10)

    ttk.Button(about_win, text="Close", command=about_win.destroy).pack(pady=20)

def main():
    global root
    root = tk.Tk()
    root.title("Hangman - Graphical Interface")
    root.geometry("600x500")
    root.configure(bg="#dfe7fd")

    main_frame = tk.Frame(root, bg="#dfe7fd")
    main_frame.pack(expand=True, fill="both")

    tk.Label(main_frame, text="Welcome to Hangman Online", 
             font=("Helvetica", 20, "bold"), bg="#dfe7fd").pack(pady=20)

    ttk.Button(main_frame, text="About", command=lambda: show_about(root)).pack(pady=10)
    ttk.Button(main_frame, text="Play", command=start_game).pack(pady=10)
    ttk.Button(main_frame, text="Add Words", command=add_words_ui).pack(pady=10)
    ttk.Button(main_frame, text="Exit", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()