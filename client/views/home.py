import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Container frame for centered content
        container = tk.Frame(self)
        container.pack(expand=True)

        # Title
        tk.Label(
            container, 
            text="Welcome to Hangman Online", 
            font=("Arial", 16)
        ).pack(pady=20, anchor="center")

        # Buttons (centered)
        buttons = [
            ("Log In", "LoginScreen"),
            ("Sign Up", "SignupScreen"),
            ("About", "AboutScreen"),
            ("Exit", None)
        ]

        for text, screen_name in buttons:
            cmd = self.controller.root.quit if screen_name is None else lambda name=screen_name: self.controller.show_screen(name)
            
            tk.Button(
                container, 
                text=text, 
                command=cmd
            ).pack(pady=5, anchor="center")

