# views/about.py
import tkinter as tk

class AboutScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        # Title Label
        tk.Label(self, text="About the App", font=("Arial", 16)).pack(pady=20)
        
        # App Description
        about_text = (
            "This is a socket-based client application.\n"
            "You can log in, sign up, create or join rooms, and interact with others.\n\n"
            "Developed as a simple demonstration of socket programming.\n\n"
            "Version 1.0"
        )
        tk.Label(self, text=about_text, justify=tk.LEFT).pack(padx=20, pady=10)
        
        # Back to Home button
        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomeScreen"))
        self.back_button.pack(pady=20)

