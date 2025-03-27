# main.py (Primer commit - Autenticación y UI)

import tkinter as tk
from tkinter import ttk, messagebox
from logic import HangmanGame, get_word_list, add_word_to_file

# ------------------------------
# Authentication & User Management
# ------------------------------
# Sample credentials for demonstration
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "player": {"password": "player123", "role": "player"}
}

def authenticate(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None

def register_user(username, password):
    if username in USERS:
        return False  # User already exists
    USERS[username] = {"password": password, "role": "player"}
    return True

# ------------------------------
# UI: Authentication Screen
# ------------------------------
def login_screen():
    login_root = tk.Tk()
    login_root.title("Hangman Authentication")
    login_root.geometry("400x300")

    tk.Label(login_root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_root)
    username_entry.pack(pady=5)

    tk.Label(login_root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_root, show="*")
    password_entry.pack(pady=5)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        role = authenticate(username, password)
        if role:
            login_root.destroy()
            if role == "admin":
                admin_ui()
            else:
                player_ui()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def on_register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username already exists")

    ttk.Button(login_root, text="Log In", command=on_login).pack(pady=10)
    ttk.Button(login_root, text="Register", command=on_register).pack(pady=5)
    login_root.mainloop()

# ------------------------------
# UI: Admin Interface
# ------------------------------
def admin_ui():
    admin_win = tk.Tk()
    admin_win.title("Admin Panel")
    admin_win.geometry("500x400")

    tk.Label(admin_win, text="Admin Panel", font=("Helvetica", 18, "bold")).pack(pady=10)
    ttk.Button(admin_win, text="Manage Words", command=add_words_ui).pack(pady=5)
    ttk.Button(admin_win, text="View Players", command=lambda: messagebox.showinfo("Players", "Feature coming soon!")).pack(pady=5)
    ttk.Button(admin_win, text="About", command=lambda: show_about(admin_win)).pack(pady=5)
    ttk.Button(admin_win, text="Exit", command=admin_win.destroy).pack(pady=10)
    admin_win.mainloop()

# ------------------------------
# UI: Player Interface
# ------------------------------
def player_ui():
    player_win = tk.Tk()
    player_win.title("Hangman - Player Menu")
    player_win.geometry("400x300")

    tk.Label(player_win, text="Welcome, Player!", font=("Helvetica", 16, "bold")).pack(pady=10)
    ttk.Button(player_win, text="About the Game", command=lambda: show_about(player_win)).pack(pady=5)
    ttk.Button(player_win, text="Play", command=main_game_ui).pack(pady=5)
    ttk.Button(player_win, text="Exit", command=player_win.destroy).pack(pady=10)
    player_win.mainloop()
# main.py (Segundo commit - Juego y Gestión de Palabras)

import tkinter as tk
from tkinter import ttk, messagebox
from logic import HangmanGame, get_word_list, add_word_to_file
import random

# ------------------------------
# Utility: Hangman ASCII Drawing
# ------------------------------
def get_hangman_drawing(errors):
    stages = [
    """
     ------  
     |    |
     |
     |
     |
     |
  --------
    """,
    """
     ------  
     |    |
     |    O
     |
     |
     |
  --------
    """,
    """
     ------  
     |    |
     |    O
     |    |
     |
     |
  --------
    """,
    """
     ------  
     |    |
     |    O
     |   /|
     |
     |
  --------
    """,
    """
     ------  
     |    |
     |    O
     |   /|\\
     |
     |
  --------
    """,
    """
     ------  
     |    |
     |    O
     |   /|\\
     |   /
     |
  --------
    """,
    """
     ------  
     |    |
     |    O
     |   /|\\
     |   / \\
     |
  --------
    """
    ]
    if errors < 0:
        errors = 0
    if errors > 6:
        errors = 6
    return stages[errors]

# ------------------------------
# UI: Main Game Interface (for Players)
# ------------------------------
def main_game_ui():
    game_win = tk.Tk()
    game_win.title("Hangman Game")
    game_win.geometry("600x500")
    game_win.configure(bg="#ffffff")

    words = get_word_list()
    game = HangmanGame(words)

    word_var = tk.StringVar(value=game.get_display_word())
    attempts_var = tk.StringVar(value=f"Attempts left: {game.attempts_left}")
    wrong_var = tk.StringVar(value="Wrong letters:")
    points_var = tk.StringVar(value=f"Points: {game.points}")
    message_var = tk.StringVar(value="")
    hangman_var = tk.StringVar(value=get_hangman_drawing(0))

    tk.Label(game_win, textvariable=hangman_var, font=("Courier", 12), bg="#ffffff", justify="left").pack(pady=5)
    tk.Label(game_win, textvariable=word_var, font=("Helvetica", 24), bg="#ffffff").pack(pady=10)
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
        errors = game.max_attempts - game.attempts_left
        hangman_var.set(get_hangman_drawing(errors))
        if game.game_over:
            letter_entry.config(state="disabled")

    ttk.Button(game_win, text="Guess", command=on_guess).pack(pady=10)
    ttk.Button(game_win, text="Close Game", command=game_win.destroy).pack(pady=10)
    game_win.mainloop()

# ------------------------------
# UI: Add Words (Management) Interface
# ------------------------------
def add_words_ui():
    add_win = tk.Toplevel()
    add_win.title("Manage Words")
    add_win.geometry("500x400")
    add_win.configure(bg="#f0f0f0")

    tk.Label(add_win, text="Manage Words", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=10)
    current_words = get_word_list()
    words_str = "\n".join(current_words)
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
    add_win.mainloop()

# ------------------------------
# UI: About Screen
# ------------------------------
def show_about(master):
    about_win = tk.Toplevel(master)
    about_win.title("About")
    about_win.geometry("655x555")
    about_win.configure(bg="#f0f0f0")

    tk.Label(about_win, text="About the Application", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)
    team_info = (
        "Team Members:\n"
        " - Emiliano Hinojosa Guzmán (0252496)\n"
        " - Diego Amin Hernández Pallares (0250146)\n"
        " - Mario Alejandro Rodriguez Gonzalez (0235810)\n\n"
        "Subject: Distributed Computing\n"
        "Professor: Dr. Juan Carlos López Pimentel\n"
        "Date: 01/04/2025\n"
    )
    tk.Label(about_win, text=team_info, font=("Helvetica", 12), justify="left", bg="#f0f0f0").pack(pady=10, padx=10)
    game_info = (
        "How to Play:\n\n"
        "The objective is to guess the hidden word letter by letter.\n"
        "You have 6 attempts. Each correct letter adds 20 points and each mistake subtracts 10 points.\n"
        "As you make mistakes, the hangman drawing progresses.\n"
        "You win if you guess the word before running out of attempts; otherwise, you lose.\n"
    )
    tk.Label(about_win, text=game_info, font=("Helvetica", 12), justify="left", bg="#f0f0f0").pack(pady=10, padx=10)
    ttk.Button(about_win, text="Close", command=about_win.destroy).pack(pady=20)
