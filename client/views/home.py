import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        # Configure the frame to expand and fill available space
        self.pack(expand=True, fill="both")
        
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
        
        for text, frame_name in buttons:
            if frame_name:
                cmd = lambda name=frame_name: controller.show_frame(name)
            else:
                cmd = master.quit
            
            tk.Button(
                container, 
                text=text, 
                command=cmd
            ).pack(pady=5, anchor="center")