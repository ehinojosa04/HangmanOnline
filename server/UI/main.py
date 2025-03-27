# primer_commit.py
import tkinter as tk
from tkinter import ttk, messagebox
from hangman_logic import HangmanGame, get_word_list, add_word_to_file

# Simulated user credentials
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
        return False
    USERS[username] = {"password": password, "role": "player"}
    return True

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
    return stages[min(errors, 6)]

# =========================
# Definición de ventanas
# =========================

def login_screen(root):
    """Login and register window (Toplevel)."""
    login_win = tk.Toplevel(root)
    login_win.title("Hangman Authentication")
    login_win.geometry("400x300")

    tk.Label(login_win, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack(pady=5)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        role = authenticate(username, password)
        if role:
            login_win.destroy()
            if role == "admin":
                admin_ui(root)
            else:
                player_ui(root)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def on_register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username already exists")

    ttk.Button(login_win, text="Log In", command=on_login).pack(pady=10)
    ttk.Button(login_win, text="Register", command=on_register).pack(pady=5)

def admin_ui(root):
    """Admin menu (Toplevel)."""
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Panel")
    admin_win.geometry("500x400")

    tk.Label(admin_win, text="Admin Panel", font=("Helvetica", 18, "bold")).pack(pady=10)
    ttk.Button(admin_win, text="Manage Words", command=lambda: add_words_ui(root)).pack(pady=5)
    ttk.Button(admin_win, text="View Players", command=lambda: messagebox.showinfo("Players", "Feature coming soon!")).pack(pady=5)
    ttk.Button(admin_win, text="About", command=lambda: show_about(root)).pack(pady=5)

    def on_exit():
        # Cerrar la app completa
        root.quit()

    ttk.Button(admin_win, text="Exit", command=on_exit).pack(pady=10)

