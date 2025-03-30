# views/signup.py
import tkinter as tk
from tkinter import messagebox

class SignupScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        # Title Label
        tk.Label(self, text="Sign Up", font=("Arial", 16)).pack(pady=20)
        
        # Username and Password input fields
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Sign Up button
        self.signup_button = tk.Button(self, text="Sign Up", command=self.sign_up)
        self.signup_button.pack(pady=10)

        # Back to Login screen button
        self.back_button = tk.Button(self, text="Back to Log In", command=lambda: controller.show_frame("LoginScreen"))
        self.back_button.pack(pady=5)

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return
        
        success, response = self.client.send_command("REGISTER", username=username, password=password)
        
        if success:
            messagebox.showinfo("Success", "Registration successful. Please log in.")
            self.controller.show_frame("LoginScreen")  # Navigate to Login screen after success
        else:
            messagebox.showerror("Error", f"Registration failed: {response}")

