import tkinter as tk
from tkinter import messagebox
import json  # Si el servidor devuelve JSON en las respuestas

class HangmanGameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e9e9e9")
        self.controller = controller
        self.client_state = self.controller.get_client_state()

        # Contenedor principal para centrar contenido
        container = tk.Frame(self, bg="#e9e9e9")
        container.pack(expand=True, padx=20, pady=20)

        # Etiqueta: Room ID
        self.room_id_label = tk.Label(
            container, 
            text="Room: ", 
            font=("Arial", 18, "bold"),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.room_id_label.pack(anchor="w", pady=5)

        # Etiqueta: Estado (Status)
        self.label_status = tk.Label(
            container, 
            text="Status: PLAYING", 
            font=("Arial", 16),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_status.pack(pady=5)

        # Canvas para dibujar la horca y el ahorcado
        self.canvas = tk.Canvas(container, width=150, height=200, bg="#e9e9e9", highlightthickness=0)
        self.canvas.pack(pady=(10, 10))

        # Etiqueta: Palabra actual
        self.label_word = tk.Label(
            container, 
            text="Word: _ _ _ _ _", 
            font=("Arial", 18),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_word.pack(pady=5)
        
        # Etiqueta: Turno
        self.label_turn = tk.Label(
            container, 
            text="Turn: Waiting...", 
            font=("Arial", 12),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_turn.pack(pady=5)
        
        # Etiqueta: Intentos restantes
        self.label_attempts = tk.Label(
            container, 
            text="Attempts Left: 6", 
            font=("Arial", 12),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_attempts.pack(pady=5)

        # Etiqueta: Puntos
        self.label_points = tk.Label(
            container,
            text="Points: 0",
            font=("Arial", 12),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_points.pack(pady=5)

        # Etiqueta: Letras equivocadas
        self.label_wrong = tk.Label(
            container,
            text="Wrong letters: ",
            font=("Arial", 12),
            fg="#333333",
            bg="#e9e9e9"
        )
        self.label_wrong.pack(pady=5)

        # Campo de entrada para la letra
        self.entry_guess = tk.Entry(container, font=("Arial", 14))
        self.entry_guess.pack(pady=5)

        # Estilo de botones uniforme
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#ffffff",
            "fg": "#333333",
            "activebackground": "#d0d0d0",
            "width": 15,
            "relief": tk.RAISED,
            "bd": 2
        }

        # Botón para enviar la conjetura
        self.guess_button = tk.Button(
            container, text="GUESS", command=self.make_guess, **button_style
        )
        self.guess_button.pack(pady=5)

        # Botón para salir del juego
        self.exit_button = tk.Button(
            container, text="EXIT GAME", command=self.exit_game, **button_style
        )
        self.exit_button.pack(pady=5)

        # Footer opcional
        footer = tk.Label(
            self,
            text="© 2026 Hangman Online",
            font=("Arial", 10),
            fg="#666666",
            bg="#e9e9e9"
        )
        footer.pack(side="bottom", pady=5)

        self.update_game_info()
    
    def update_game_info(self):
        """Actualiza la interfaz con la información actual del juego almacenada en room_data."""
        game_data = self.client_state.room_data  
        
        # Extraer y formatear la palabra adivinada
        guessed_letters = game_data.get('guessed_letters', '_____')
        formatted_word = " ".join(guessed_letters)
        
        # Obtener otros campos del estado del juego
        status = game_data.get('status', 'PLAYING')
        turn = game_data.get('turn', 'Waiting...')
        attempts_left = game_data.get('attempts', 6)
        points = game_data.get('points', 0)
        wrong_letters = game_data.get('wrong_letters', "")
        
        # Actualizar etiquetas
        self.room_id_label.config(text=f"Room: {game_data.get('index', 'Unknown')}")
        self.label_status.config(text=f"Status: {status}")
        self.label_word.config(text=f"Word: {formatted_word}")
        self.label_turn.config(text=f"Turn: {turn}")
        self.label_attempts.config(text=f"Attempts Left: {attempts_left}")
        self.label_points.config(text=f"Points: {points}")
        self.label_wrong.config(text=f"Wrong letters: {wrong_letters}")
        
        # Calcular errores basados en intentos restantes (6 intentos totales)
        errors = 6 - int(attempts_left)
        self.draw_hangman(errors)

    def draw_hangman(self, errors):
        """Dibuja la horca y las partes del cuerpo según el número de errores."""
        self.canvas.delete("all")
        # Dibujar la estructura fija de la horca
        self.canvas.create_line(20, 180, 130, 180, width=4, fill="#333333")   # Base
        self.canvas.create_line(50, 180, 50, 20, width=4, fill="#333333")     # Poste
        self.canvas.create_line(50, 20, 110, 20, width=4, fill="#333333")     # Viga
        self.canvas.create_line(110, 20, 110, 40, width=4, fill="#333333")    # Cuerda

        # Dibujar partes del cuerpo según el número de errores
        if errors >= 1:  # Cabeza
            self.canvas.create_oval(95, 40, 125, 70, width=4, outline="#333333")
        if errors >= 2:  # Cuerpo
            self.canvas.create_line(110, 70, 110, 120, width=4, fill="#333333")
        if errors >= 3:  # Brazo izquierdo
            self.canvas.create_line(110, 80, 80, 100, width=4, fill="#333333")
        if errors >= 4:  # Brazo derecho
            self.canvas.create_line(110, 80, 140, 100, width=4, fill="#333333")
        if errors >= 5:  # Pierna izquierda
            self.canvas.create_line(110, 120, 90, 150, width=4, fill="#333333")
        if errors >= 6:  # Pierna derecha
            self.canvas.create_line(110, 120, 130, 150, width=4, fill="#333333")

    def make_guess(self):
        """Envía la letra conjeturada al servidor y actualiza la interfaz."""
        guess = self.entry_guess.get().strip()
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single letter.")
            return
        
        success, response = self.client_state.send_command(f"GUESS_{guess}")
        if success:
            # Si el servidor envía datos actualizados en JSON, parseamos la respuesta
            try:
                data = json.loads(response)
                self.client_state.room_data.update(data)
            except Exception:
                # Si la respuesta no es JSON, asumimos que room_data ya fue actualizado
                pass
            self.update_game_info()
        else:
            messagebox.showerror("Error", f"Failed to send guess: {response}")
        self.entry_guess.delete(0, tk.END)

    def exit_game(self):
        """Sale del juego y regresa al menú principal."""
        success, response = self.client_state.send_command("EXIT")
        if success:
            messagebox.showinfo("Exited Game", "You have left the game.")
            self.client_state.room_data = {}
            self.controller.show_screen("MainMenuScreen")
        else:
            messagebox.showerror("Error", f"Failed to exit game: {response}")
