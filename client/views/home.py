import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        tk.Label(self, text="Welcome to the Socket Client", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self, text="Log In", command=lambda: controller.show_frame("LoginScreen")).pack(pady=5)
        tk.Button(self, text="Sign Up", command=lambda: controller.show_frame("SignupScreen")).pack(pady=5)
        tk.Button(self, text="About", command=lambda: controller.show_frame("AboutScreen")).pack(pady=5)
        tk.Button(self, text="Exit", command=master.quit).pack(pady=5)

