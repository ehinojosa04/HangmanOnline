# views/main_menu.py
import tkinter as tk
from tkinter import messagebox, simpledialog

class MainMenuScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        # Title Label
        self.title_label = tk.Label(self, text=f"Welcome, {self.client.get_username()}", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Room Info Label
        self.room_label = tk.Label(self, text="")
        self.room_label.pack(pady=10)

        # Buttons
        self.create_room_button = tk.Button(self, text="Create Room", command=self.create_room)
        self.join_room_button = tk.Button(self, text="Join Room", command=self.join_room)
        self.enter_room_button = tk.Button(self, text="Enter Room", command=self.enter_room)
        self.logout_button = tk.Button(self, text="Log Out", command=self.logout)
        self.exit_button = tk.Button(self, text="Exit", command=master.quit)

        self.create_room_button.pack(pady=5)
        self.join_room_button.pack(pady=5)
        self.enter_room_button.pack(pady=5)
        self.logout_button.pack(pady=5)
        self.exit_button.pack(pady=5)

    def update_ui(self):
        """Update UI elements dynamically."""
        username = self.client.get_username()
        room_id = self.client.get_current_room()

        self.title_label.config(text=f"Welcome, {username}")
        
        if room_id:
            self.room_label.config(text=f"Current Room: {room_id}")
            self.enter_room_button.pack(pady=5)
        else:
            self.room_label.config(text="Not in a room")
            self.enter_room_button.pack_forget()

    def create_room(self):
        success, response = self.client.send_command("CREATE")
        if success:
            messagebox.showinfo("Success", f"Room created with ID: {response}")
            self.client.roomID = response.strip()  # Store the room ID
            self.controller.show_frame("RoomScreen", room_info=self.get_room_info())
        else:
            messagebox.showerror("Error", f"Failed to create room: {response}")

    def join_room(self):
        room_id = simpledialog.askstring("Room ID", "Enter Room ID to join:")
        
        if room_id:
            success, response = self.client.send_command("JOIN", roomID=room_id)
            if success:
                messagebox.showinfo("Success", f"Joined room {room_id}")
                self.client.roomID = room_id  # Store the room ID
                self.controller.show_frame("RoomScreen", room_info=self.get_room_info())
            else:
                messagebox.showerror("Error", f"Failed to join room: {response}")

    def enter_room(self):
        """Navigate to the room screen."""
        self.controller.show_frame("RoomScreen", room_info=self.get_room_info())

    def get_room_info(self):
        """Mock function to fetch room details. Should be replaced with actual server query."""
        return {
            "index": self.client.get_current_room(),
            "admin": {"username": self.client.username},  # Assuming admin is the creator
            "users": [],  # Placeholder, should fetch real user list from server
            "n_users": 1,  # Placeholder
            "isPrivate": False,  # Placeholder
            "status": 0  # Waiting
        }

    def logout(self):
        success, response = self.client.send_command("LOGOUT")
        if success:
            messagebox.showinfo("Success", "You have logged out.")
            self.client.disconnect()
            self.controller.show_frame("HomeScreen")
        else:
            messagebox.showerror("Error", f"Logout failed: {response}")

