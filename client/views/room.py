import tkinter as tk

class RoomScreen(tk.Frame):
    def __init__(self, parent, gui_manager):
        super().__init__(parent)
        self.gui_manager = gui_manager

        # UI Elements
        self.label_status = tk.Label(self, text="Status: ", font=("Arial", 14))
        self.label_status.pack(pady=5)

        self.label_players = tk.Label(self, text="Players: ", font=("Arial", 12))
        self.label_players.pack(pady=5)

        self.label_word = tk.Label(self, text="Word: ", font=("Arial", 12))
        self.label_word.pack(pady=5)

    def update_room_info(self):
        """Fetch latest data from ClientState and update UI."""
        client_state = self.gui_manager.get_client_state()
        room_data = client_state.room_data  # Fetch stored room info

        status = room_data.get("status", "UNKNOWN")
        players = ", ".join(room_data.get("players", []))
        word = room_data.get("word", "")

        # Update labels
        self.label_status.config(text=f"Status: {status}")
        self.label_players.config(text=f"Players: {players}")

        if status == "PLAYING":
            self.label_word.config(text=f"Word: {word}")
            self.label_word.pack()
        else:
            self.label_word.pack_forget()  # Hide word label when not playing
