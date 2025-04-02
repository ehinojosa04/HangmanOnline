import tkinter as tk
from tkinter import messagebox

class HangmanGameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.client_state = self.controller.get_client_state()

        # UI Elements
        self.room_id_label = tk.Label(self, text="Room: ", font=("Arial", 14))
        self.room_id_label.pack(anchor="nw", padx=10, pady=5)

        self.label_status = tk.Label(self, text="Status: PLAYING", font=("Arial", 14))
        self.label_status.pack(pady=5)

        self.label_word = tk.Label(self, text="Word: _ _ _ _ _", font=("Arial", 18))
        self.label_word.pack(pady=5)
        
        self.label_turn = tk.Label(self, text="Turn: Waiting...", font=("Arial", 12))
        self.label_turn.pack(pady=5)
        
        self.label_attempts = tk.Label(self, text="Attempts Left: 6", font=("Arial", 12))
        self.label_attempts.pack(pady=5)

        self.entry_guess = tk.Entry(self, font=("Arial", 14))
        self.entry_guess.pack(pady=5)
        
        self.guess_button = tk.Button(self, text="GUESS", command=self.make_guess)
        self.guess_button.pack()
        
        self.exit_button = tk.Button(self, text="EXIT GAME", command=self.exit_game)
        self.exit_button.pack()

    def update_game_info(self):
        """Fetch latest game state from ClientState and update UI."""
        game_data = self.client_state.room_data  # Fetch stored game info
        
        self.room_id_label.config(text=f"Room: {game_data.get('index', 'Unknown')}")
        self.label_word.config(text=f"Word: {game_data.get('word', '_ _ _ _ _')}")
        self.label_turn.config(text=f"Turn: {game_data.get('turn', 'Waiting...')}")
        self.label_attempts.config(text=f"Attempts Left: {game_data.get('attempts_left', 6)}")
        
        self.entry_guess.config(state="normal")
        self.guess_button.config(state="normal")
        # Enable/disable guess input based on turn
        '''
        if game_data.get("turn") == self.client_state.username:
            self.entry_guess.config(state="normal")
            self.guess_button.config(state="normal")
        else:
            self.entry_guess.config(state="disabled")
            self.guess_button.config(state="disabled")
        '''

    def make_guess(self):
        """Send the guessed letter to the server."""
        guess = self.entry_guess.get().strip()
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single letter.")
            return
        
        success, response = self.client_state.send_command(f"GUESS_{guess}")
        if not success:
            messagebox.showerror("Error", f"Failed to send guess: {response}")
        self.entry_guess.delete(0, tk.END)

    def exit_game(self):
        """Exit the game and return to the main menu."""
        success, response = self.client_state.send_command("EXIT")
        if success:
            messagebox.showinfo("Exited Game", "You have left the game.")
            self.client_state.game_data = {}
            self.controller.show_screen("MainMenuScreen")
        else:
            messagebox.showerror("Error", f"Failed to exit game: {response}")
