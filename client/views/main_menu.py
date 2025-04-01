import tkinter as tk
from tkinter import messagebox, simpledialog

class MainMenuScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Title Label
        self.title_label = tk.Label(self, text="Welcome", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Room Info Label
        self.room_label = tk.Label(self, text="Not in a room")
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
        """Update UI elements dynamically based on client state."""
        client_state = self.controller.get_client_state()
        username = client_state.username
        room_data = client_state.room_data  # Pull room data from ClientState

        self.title_label.config(text=f"Welcome, {username if username else 'Guest'}")

        if room_data and "index" in room_data:
            room_id = room_data["index"]
            self.room_label.config(text=f"Current Room: {room_id}")
            self.enter_room_button.pack(pady=5)
        else:
            self.room_label.config(text="Not in a room")
            self.enter_room_button.pack_forget()

    def create_room(self):
        """Create a new room and update the UI."""
        client_state = self.controller.get_client_state()
        success, response = client_state.send_command("CREATE")
        if success:
            client_state.roomID = response.strip()
            client_state.room_data = {"index": client_state.roomID, "users": [client_state.username]}
            self.update_ui()
            self.controller.show_screen("RoomScreen")
        else:
            messagebox.showerror("Error", f"Failed to create room: {response}")

    def join_room(self):
        """Join an existing room and update UI."""
        client_state = self.controller.get_client_state()
        room_id = simpledialog.askstring("Room ID", "Enter Room ID to join:")
        if room_id and room_id.isdigit():
            success, response = client_state.send_command("JOIN", roomID=room_id)
            if success:
                client_state.roomID = room_id
                client_state.room_data = {"index": room_id, "users": [client_state.username]}
                self.update_ui()
                self.controller.show_screen("RoomScreen")
            else:
                messagebox.showerror("Error", f"Failed to join room {room_id}:\n{response}")
        else:
            messagebox.showerror("Error", "Room ID must be a number")

    def enter_room(self):
        """Enter the room based on stored client data."""
        client_state = self.controller.get_client_state()
        if client_state.room_data:
            self.controller.show_screen("RoomScreen")
        else:
            messagebox.showerror("Error", "You are not in a room.")

    def logout(self):
        """Log out the user and return to HomeScreen."""
        client_state = self.controller.get_client_state()
        success, response = client_state.send_command("LOGOUT")
        if success:
            messagebox.showinfo("Success", "You have logged out.")
            client_state.roomID = ""
            client_state.room_data = {}
            client_state.disconnect()
            self.controller.show_screen("HomeScreen")
        else:
            messagebox.showerror("Error", f"Logout failed: {response}")

