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

if __name__ == "__main__":
    login_screen()
