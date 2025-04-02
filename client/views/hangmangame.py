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
    
        
    def show_popup(self):
        # Verificar si ya existe un popup abierto
        if hasattr(self, 'popup') and self.popup.winfo_exists():
            return
            
        self.popup = tk.Toplevel(self)
        self.popup.title("Confirmation")
        self.popup.geometry("300x150")
        self.popup.resizable(False, False)
        
        # Hacer el popup modal
        self.popup.grab_set()
        
        label = tk.Label(self.popup, text="Do you want to exit?", font=("Arial", 12))
        label.pack(pady=10)
        
        # Usar lambda para evitar llamada inmediata
        btn_stay = tk.Button(
            self.popup, 
            text="Stay in Room", 
            command=lambda: self.controller.show_screen("RoomScreen")
        )
        btn_stay.pack(side=tk.LEFT, padx=20, pady=10)

        btn_exit = tk.Button(
            self.popup, 
            text="Exit", 
            command=self.exit_game
        )
        btn_exit.pack(side=tk.RIGHT, padx=20, pady=10)

    def update_game_info(self):
        """Fetch latest game state from ClientState and update UI."""
        game_data = self.client_state.room_data  # Fetch stored game info
        
        guessed_letters = game_data.get('guessed_letters', '_____')
        formatted_word = " ".join(guessed_letters)

        self.room_id_label.config(text=f"Room: {game_data.get('index', 'Unknown')}")
        self.label_word.config(text=f"Word: {formatted_word}")
        self.label_turn.config(text=f"Turn: {game_data.get('turn', 'Waiting...')}")
        self.label_attempts.config(text=f"Attempts Left: {game_data.get('attempts', '6')}")
        
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

        if game_data.get("status", "unknown") == "WAITING":
            if not hasattr(self, 'popup') or not self.popup.winfo_exists():
                #self.show_popup()
                pass


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
