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
