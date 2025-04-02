import tkinter as tk
from tkinter import messagebox

class RoomScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.client_state = self.controller.get_client_state()

        # UI Elements

        self.room_id_label = tk.Label(self, text="Room: ", font=("Arial", 14))
        self.room_id_label.pack(anchor="nw", padx=10, pady=5)

        self.label_status = tk.Label(self, text="Status: ", font=("Arial", 14))
        self.label_status.pack(pady=5)

        self.label_players = tk.Label(self, text="Players:\n\n", font=("Arial", 12))
        self.label_players.pack(pady=5)

        self.label_word = tk.Label(self, text="Word: ", font=("Arial", 12))
        self.label_word.pack(pady=5)

        self.start_button = tk.Button(self, text="START", command=self.start_game)
        self.exit_button = tk.Button(self, text="EXIT ROOM", command=self.exit_room)


    def update_room_info(self):
        room_data = self.client_state.room_data  

        room_index = room_data.get("index", "index not found")
        status = room_data.get("status", "UNKNOWN")
        admin = room_data.get("admin", "admin unknown")
        players = "->" + "\n".join(room_data.get("players", []))
        word = room_data.get("word", "")

        self.room_id_label.config(text=f"Room: {room_index}")
        self.label_status.config(text=f"Status: {status}")
        self.label_players.config(text=f"Players:\n\n{players}")

        if status == "PLAYING":
            self.label_word.config(text=f"Word: {word}")
            self.label_word.pack()
            self.exit_button.pack_forget()
            self.label_players.config(anchor="ne", justify="right")

        # Automatically switch to the game screen
            self.controller.show_screen("HangmanGameScreen")

        else:
            if admin == self.client_state.username and status == "WAITING":
                self.start_button.pack()
            else:
                self.start_button.pack_forget()

            self.label_word.pack_forget()
            self.exit_button.pack()



    def start_game(self):
        """Send command to start the game."""
        success, response = self.client_state.send_command("START")
        if success:
            messagebox.showinfo("Game Started", "The game has started!")
        else:
            messagebox.showerror("Error", f"Failed to start game: {response}")


    def exit_room(self):
        """Exit the current room."""
        success, response = self.client_state.send_command("EXIT")
        if success:
            messagebox.showinfo("Exited Room", "You have left the room.")
            self.client_state.room_data = {}
            self.controller.show_screen("MainMenuScreen")
        else:
            messagebox.showerror("Error", f"Failed to exit room: {response}")

