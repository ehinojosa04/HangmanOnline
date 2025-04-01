# views/about.py
import tkinter as tk

class AboutScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Title Label
        tk.Label(self, text="About the App", font=("Arial", 16)).pack(pady=20)
        
        # App Description
        about_text = (
            "This project is an online version of the classic Hangman game. \n"
            "In Hangman, one player thinks of a word, and the other players try to guess it \n letter by letter before running out of attempts. \n"
            "You can log in, sign up, create or join rooms, and interact with others in Hangman Online.\n\n"
            "Developed By:\n"
            " - Emiliano Hinojosa Guzmán - ID: 0252496\n"
            " - Diego Amin Hernández Pallares - ID: 0250146\n"
            " - Mario Alejandro Rodriguez Gonzalez - ID:0235810\n\n"
            "Subject: Distributed Computing\n"
            "Professor: Dr. Juan Carlos López Pimentel\n"
            "Date: 03/04/2025\n"
            "Version 1.0"
        )
        tk.Label(self, text=about_text, justify=tk.LEFT).pack(padx=20, pady=10)
        
        # Back to Home button
        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_screen("HomeScreen"))
        self.back_button.pack(pady=20)

