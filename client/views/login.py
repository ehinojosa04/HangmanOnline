import tkinter as tk

class LoginScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

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
        tk.Button(self, text="Back", command=lambda: controller.show_screen("HomeScreen")).pack(pady=5)

    def login(self):
        client = self.controller.get_client_state()  # Get client state from controller
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, response = client.send_command("LOGIN", username=username, password=password)
        if success:
            client.username = username
            print(f"DEBUG: Username set to: {client.username}")  # Debugging output
            self.controller.show_screen("MainMenuScreen")
        else:
            self.message_label.config(text=response)

