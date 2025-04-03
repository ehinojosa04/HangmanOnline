import tkinter as tk

class LoginScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#e9e9e9")
        self.controller = controller
        container = tk.Frame(self, bg="#e9e9e9")
        container.pack(expand=True)
        canvas = tk.Canvas(container, width=150, height=200, bg="#e9e9e9", highlightthickness=0)
        canvas.pack(pady=(20, 10))
        
        title_label = tk.Label(
            container, #cambios
            text="Welcome to Hangman Online",
            font=("Arial", 20, "bold"),
            fg="#333333",
            bg="#e9e9e9"
        )
        title_label.pack(pady=(10, 20))
        
        header_label = tk.Label(
            container,
            text="Log In",
            font=("Arial", 16, "bold"),
            fg="#333333",
            bg="#e9e9e9"
        )
        header_label.pack(pady=5)
        label_style = {"font": ("Arial", 12), "bg": "#e9e9e9", "fg": "#333333"}
        entry_style = {"font": ("Arial", 12)}
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#ffffff",
            "fg": "#333333",
            "activebackground": "#d0d0d0",
            "width": 15,
            "relief": tk.RAISED,
            "bd": 2
        }
        
        tk.Label(container, text="Username:", **label_style).pack()
        self.username_entry = tk.Entry(container, **entry_style)
        self.username_entry.pack(pady=5)
        
        tk.Label(container, text="Password:", **label_style).pack()
        self.password_entry = tk.Entry(container, show="*", **entry_style)
        self.password_entry.pack(pady=5)
        
        self.message_label = tk.Label(container, text="", fg="red", bg="#e9e9e9", font=("Arial", 11))
        self.message_label.pack(pady=5)
        
        tk.Button(container, text="Log In", command=self.login, **button_style).pack(pady=5)
        tk.Button(container, text="Back to Home", command=lambda: controller.show_screen("HomeScreen"), **button_style).pack(pady=5)
        
    def login(self):
        client = self.controller.get_client_state()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        success, response = client.send_command("LOGIN", username=username, password=password)
        if success:
            client.username = username
            print(f"DEBUG: Username set to: {client.username}")
            self.controller.show_screen("MainMenuScreen")
        else:
            self.message_label.config(text=response)