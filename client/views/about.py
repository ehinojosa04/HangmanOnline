import tkinter as tk

class AboutScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#e9e9e9")  
        self.controller = controller
        container = tk.Frame(self, bg="#e9e9e9")
        container.pack(expand=True)

        title_label = tk.Label(
            container,
            text="About the App",
            font=("Arial", 20, "bold"),
            fg="#333333",
            bg="#e9e9e9"
        )
        title_label.pack(pady=(10, 20))
        about_text = (
            "This project is an online version of the classic Hangman game.\n"
            "In Hangman, one player thinks of a word, and the other players\n"
            "try to guess it letter by letter before running out of attempts.\n\n"
            "You can log in, sign up, create or join rooms, and interact\n"
            "with others in Hangman Online.\n\n"
            "Developed By:\n"
            " - Emiliano Hinojosa Guzmán - ID: 0252496\n"
            " - Diego Amin Hernández Pallares - ID: 0250146\n"
            " - Mario Alejandro Rodriguez Gonzalez - ID: 0235810\n\n"
            "Subject: Distributed Computing\n"
            "Professor: Dr. Juan Carlos López Pimentel\n"
            "Date: 03/04/2025\n"
            "Version 1.0"
        )

        about_label = tk.Label(
            container,
            text=about_text,
            justify=tk.CENTER,     
            font=("Arial", 12),
            fg="#333333",
            bg="#e9e9e9"
        )
        about_label.pack(padx=20, pady=10)
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#ffffff",
            "fg": "#333333",
            "activebackground": "#d0d0d0",
            "width": 15,
            "relief": tk.RAISED,
            "bd": 2
        }
        back_button = tk.Button(
            container,
            text="Back to Home",
            command=lambda: controller.show_screen("HomeScreen"),
            **button_style
        )
        back_button.pack(pady=20)
        footer = tk.Label(
            self,
            text="© 2026 Hangman Online",
            font=("Arial", 11),
            fg="#666666",
            bg="#e9e9e9"
        )
        footer.pack(side="bottom", pady=5) #cambios