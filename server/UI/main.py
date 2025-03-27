import tkinter as tk
from tkinter import ttk, messagebox

# Credenciales de prueba
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
        return False  # Usuario ya existe
    USERS[username] = {"password": password, "role": "player"}
    return True

def login_screen():
    root = tk.Tk()
    root.title("Hangman Authentication")
    root.geometry("400x300")

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        role = authenticate(username, password)
        if role:
            root.destroy()
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

    ttk.Button(root, text="Log In", command=on_login).pack(pady=10)
    ttk.Button(root, text="Register", command=on_register).pack(pady=5)
    root.mainloop()

    from tkinter import ttk, messagebox
    from logic import HangmanGame, get_word_list, add_word_to_file  

def admin_ui():
    admin_win = tk.Tk()
    admin_win.title("Admin Panel")
    admin_win.geometry("500x400")

    tk.Label(admin_win, text="Admin Panel", font=("Helvetica", 18, "bold")).pack(pady=10)
    ttk.Button(admin_win, text="Manage Words", command=add_words_ui).pack(pady=5)
    ttk.Button(admin_win, text="View Players", command=lambda: messagebox.showinfo("Players", "Feature coming soon!"))
    ttk.Button(admin_win, text="Exit", command=admin_win.destroy).pack(pady=10)
    admin_win.mainloop()

def player_ui():
    player_win = tk.Tk()
    player_win.title("Hangman - Player Menu")
    player_win.geometry("400x300")

    tk.Label(player_win, text="Welcome, Player!", font=("Helvetica", 16, "bold")).pack(pady=10)
    ttk.Button(player_win, text="About the Game", command=lambda: messagebox.showinfo("About", "Hangman Game"))
    ttk.Button(player_win, text="Play", command=main_game_ui).pack(pady=5)
    ttk.Button(player_win, text="Exit", command=player_win.destroy).pack(pady=10)
    player_win.mainloop()

def main_game_ui():
    game_win = tk.Tk()
    game_win.title("Hangman Game")
    game_win.geometry("600x400")

    words = get_word_list()
    game = HangmanGame(words)
    word_var = tk.StringVar(value=game.get_display_word())
    tk.Label(game_win, textvariable=word_var, font=("Helvetica", 24)).pack(pady=20)

    def on_guess():
        pass 
    ttk.Button(game_win, text="Play", command=on_guess).pack(pady=10)
    game_win.mainloop()

def add_words_ui():
    add_win = tk.Toplevel()
    add_win.title("Manage Words")
    add_win.geometry("500x400")

    tk.Label(add_win, text="Manage Words", font=("Helvetica", 14)).pack(pady=10)
    new_word_entry = tk.Entry(add_win, font=("Helvetica", 14))
    new_word_entry.pack(pady=5)

    def on_add():
        new_word = new_word_entry.get().strip()
        add_word_to_file(new_word)
        messagebox.showinfo("Success", "Word Added!")

    ttk.Button(add_win, text="Add", command=on_add).pack(pady=10)
    ttk.Button(add_win, text="Close", command=add_win.destroy).pack(pady=10)
    add_win.mainloop()


if __name__ == "__main__":
    login_screen()
