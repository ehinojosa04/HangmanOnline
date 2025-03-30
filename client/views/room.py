# views/room.py
import tkinter as tk
from tkinter import messagebox

class RoomScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        self.room_label = tk.Label(self, text="", font=("Arial", 16))
        self.room_label.pack(pady=10)

        self.admin_label = tk.Label(self, text="", font=("Arial", 12))
        self.admin_label.pack(pady=5)

        self.users_label = tk.Label(self, text="", font=("Arial", 12))
        self.users_label.pack(pady=5)

        self.private_label = tk.Label(self, text="", font=("Arial", 12))
        self.private_label.pack(pady=5)

        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.start_game_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.leave_button = tk.Button(self, text="Leave Room", command=self.leave_room)

    def update_ui(self, room_info):
        """
        Update UI based on room information.

        Args:
            room_info (dict): Contains room details from the server.
        """
        room_id = room_info["index"]
        admin = room_info["admin"]["username"]
        users = room_info["users"]
        n_users = room_info["n_users"]
        is_private = "Yes" if room_info["isPrivate"] else "No"
        status = "In Progress" if room_info["status"] else "Waiting"

        self.room_label.config(text=f"Room ID: {room_id}")
        self.admin_label.config(text=f"Admin: {admin}")
        self.users_label.config(text=f"Users: {n_users}/4")
        self.private_label.config(text=f"Private: {is_private}")
        self.status_label.config(text=f"Status: {status}")

        if self.client.username == admin:  # If user is the admin
            self.start_game_button.pack(pady=10)
            self.leave_button.pack_forget()
        else:
            self.start_game_button.pack_forget()
            self.leave_button.pack(pady=10)

    def start_game(self):
        messagebox.showinfo("Game", "Game starting... (Placeholder)")

    def leave_room(self):
        success, response = self.client.send_command("EXIT", roomID=self.client.get_current_room())
        if success:
            messagebox.showinfo("Success", "You have left the room.")
            self.controller.show_frame("MainMenuScreen")
        else:
            messagebox.showerror("Error", f"Failed to leave room: {response}")

