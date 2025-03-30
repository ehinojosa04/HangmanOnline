import tkinter as tk

class LoginScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        tk.Label(self, text="Log In", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        
        self.message_label = tk.Label(self, text="", fg="red")
        self.message_label.pack()
        
        tk.Button(self, text="Log In", command=self.login).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("HomeScreen")).pack(pady=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, response = self.client.send_command("LOGIN", username, password)
        
        if success:
            self.controller.show_frame("MainMenuScreen")
        else:
            self.message_label.config(text=response)

