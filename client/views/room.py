import tkinter as tk
from tkinter import messagebox

class RoomScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e9e9e9")
        self.controller = controller
        self.client_state = self.controller.get_client_state()

        container = tk.Frame(self, bg="#e9e9e9")
        container.pack(expand=True, padx=20, pady=20)

        self.room_id_label = tk.Label(
            container, 
            text="Room: ", 
            font=("Arial", 18, "bold"),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.room_id_label.pack(anchor="w", pady=5)
        
        self.label_status = tk.Label(
            container, 
            text="Status: ", 
            font=("Arial", 16),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_status.pack(anchor="w", pady=5)
        
        self.label_players = tk.Label(
            container, 
            text="Players:\n\n", 
            font=("Arial", 14),
            fg="#333333",
            bg="#e9e9e9",
            justify=tk.LEFT
        )
        self.label_players.pack(anchor="w", pady=5)
        
        self.label_word = tk.Label(
            container, 
            text="Word: ", 
            font=("Arial", 14),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_word.pack(anchor="w", pady=5)
        self.label_word.pack_forget()  

        self.button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#ffffff",
            "fg": "#333333",
            "activebackground": "#d0d0d0",
            "width": 15,
            "relief": tk.RAISED,
            "bd": 2
        }
        
        self.start_button = tk.Button(
            container, text="START", command=self.start_game, **self.button_style
        )
        self.start_button.pack(pady=10)
        self.start_button.pack_forget()  
        
        self.exit_button = tk.Button(
            container, text="EXIT ROOM", command=self.exit_room, **self.button_style
        )
        self.exit_button.pack(pady=10)
        
        self.back_menu_button = tk.Button(
            container, text="Back to Menu", command=lambda: self.controller.show_screen("MainMenuScreen"), **self.button_style
        )
        self.back_menu_button.pack(pady=10)
        
        footer = tk.Label(
            self,
            text="© 2026 Hangman Online",
            font=("Arial", 10),
            fg="#666666",
            bg="#e9e9e9"
        )
        footer.pack(side="bottom", pady=5)

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
            self.label_word.pack(anchor="w", pady=5)
            self.exit_button.pack_forget()
            self.label_players.config(anchor="e", justify="right")
            self.controller.show_screen("HangmanGameScreen")
        else:
            if admin == self.client_state.username and status == "WAITING":
                self.start_button.pack(pady=10)
            else:
                self.start_button.pack_forget()
            self.label_word.pack_forget()
            self.exit_button.pack(pady=10)

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
