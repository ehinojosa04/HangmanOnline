import tkinter as tk
from tkinter import messagebox

class SignupScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#e9e9e9")  
        self.controller = controller
        self.client = controller.get_client_state()
        container = tk.Frame(self, bg="#e9e9e9")
        container.pack(expand=True)
        canvas = tk.Canvas(container, width=150, height=200, bg="#e9e9e9", highlightthickness=0)
        canvas.pack(pady=(20, 10))
        canvas.create_line(20, 180, 130, 180, width=4, fill="#333333")   
        canvas.create_line(50, 180, 50, 20, width=4, fill="#333333")      
        canvas.create_line(50, 20, 110, 20, width=4, fill="#333333")       
        canvas.create_line(110, 20, 110, 40, width=4, fill="#333333")     
        title_label = tk.Label(
            container,
            text="Sign Up",
            font=("Arial", 20, "bold"),
            fg="#333333",
            bg="#e9e9e9"
        )
        title_label.pack(pady=(10, 20))
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#ffffff",
            "fg": "#333333",
            "activebackground": "#d0d0d0",
            "width": 15,
            "relief": tk.RAISED,
            "bd": 2
        }
        username_label = tk.Label(container, text="Username:", font=("Arial", 12), bg="#e9e9e9")
        username_label.pack()
        self.username_entry = tk.Entry(container, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(container, text="Password:", font=("Arial", 12), bg="#e9e9e9")
        password_label.pack()
        self.password_entry = tk.Entry(container, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        signup_button = tk.Button(
            container, 
            text="Sign Up", 
            command=self.sign_up,
            **button_style
        )
        signup_button.pack(pady=10)
        back_login_button = tk.Button(
            container, 
            text="Back to Log In", 
            command=lambda: controller.show_screen("LoginScreen"),
            **button_style
        )
        back_login_button.pack(pady=5)

        back_home_button = tk.Button(
            container,
            text="Back to Home",
            command=lambda: controller.show_screen("HomeScreen"),
            **button_style
        )
        back_home_button.pack(pady=5)

        footer = tk.Label(
            self,
            text="Â© 2025 Hangman Online",
            font=("Arial", 11),
            fg="#666666",
            bg="#e9e9e9"
        )
        footer.pack(side="bottom", pady=5)

    def sign_up(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return
        
        success, response = self.client.send_command("REGISTER", username=username, password=password)
        
        if success:
            messagebox.showinfo("Success", "Registration successful. Please log in.")
            self.controller.show_screen("LoginScreen")
        else:
            messagebox.showerror("Error", f"Registration failed: {response}") #cambios