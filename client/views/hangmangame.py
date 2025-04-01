import tkinter as tk
from tkinter import messagebox, Button, Label, Frame, Entry, StringVar, Text
import random
import os

class HangmanGameScreen(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Variables del juego
        self.word_var = StringVar()
        self.attempts_var = StringVar()
        self.wrong_var = StringVar()
        self.points_var = StringVar(value="Points: 0")
        self.message_var = StringVar()
        
        # Variables de la lógica del juego
        self.secret_word = ""
        self.guessed = []
        self.wrong_letters = []
        self.max_attempts = 6
        self.attempts_left = 6
        self.game_over = False
        self.points = 0
        
        # Configurar la UI
        self.setup_ui()
    
    def get_hangman_drawing(self, errors):
        stages = [
            """
         ------   
         |    |   
         |        
         |        
         |        
         |        
      --------
            """,
            """
         ------   
         |    |   
         |    O   
         |        
         |        
         |        
      --------
            """,
            """
         ------   
         |    |   
         |    O   
         |    |   
         |        
         |        
      --------
            """,
            """
         ------   
         |    |   
         |    O   
         |   /|   
         |        
         |        
      --------
            """,
            """
         ------   
         |    |   
         |    O   
         |   /|\\  
         |        
         |        
      --------
            """,
            """
         ------   
         |    |   
         |    O   
         |   /|\\  
         |   /    
         |        
      --------
            """,
            """
         ------   
         |    |   
         |    O   
         |   /|\\  
         |   / \\  
         |        
      --------
            """
        ]
        return stages[min(errors, 6)]
    
    def setup_ui(self):
        # Configuración de la interfaz principal del juego
        self.title_label = Label(self, text="Hangman Game", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)
        
        # Widget para mostrar el dibujo del ahorcado
        self.hangman_drawing = Text(self, font=("Courier", 12), width=30, height=10, relief="flat")
        self.hangman_drawing.pack(pady=5)
        self.hangman_drawing.insert("1.0", self.get_hangman_drawing(0))
        self.hangman_drawing.config(state="disabled")
        
        # Etiqueta para la palabra que se está adivinando
        Label(self, textvariable=self.word_var, font=("Helvetica", 24),).pack(pady=10)
        
        # Etiquetas de información
        Label(self, textvariable=self.attempts_var, font=("Helvetica", 14)).pack(pady=5)
        Label(self, textvariable=self.wrong_var, font=("Helvetica", 14)).pack(pady=5)
        Label(self, textvariable=self.points_var, font=("Helvetica", 14)).pack(pady=5)
        Label(self, textvariable=self.message_var, font=("Helvetica", 16), fg="red").pack(pady=10)
        
        # Campo de entrada para la letra
        self.letter_entry = Entry(self, font=("Helvetica", 16), width=5, justify="center")
        self.letter_entry.pack(pady=10)
        self.letter_entry.bind("<Return>", lambda event: self.on_guess())
        
        # Frame para los botones
        button_frame = Frame(self)
        button_frame.pack(pady=10)
        
        # Botones
        Button(button_frame, text="Guess", command=self.on_guess, font=("Helvetica", 12)).grid(row=0, column=0, padx=10)
        Button(button_frame, text="New Game", command=self.start_game, font=("Helvetica", 12)).grid(row=0, column=1, padx=10)
        Button(button_frame, text="Back to Menu", command=self.back_to_menu, font=("Helvetica", 12)).grid(row=0, column=2, padx=10)
    
    def get_word_list(self, filename="words.txt"):
        """Retorna una lista de palabras del archivo."""
        default_words = ["python", "hangman", "computer", "programming", "keyboard", "developer", "challenge"]
        
        if not os.path.exists(filename):
            return default_words
            
        try:
            with open(filename, "r") as f:
                words = [line.strip() for line in f if line.strip()]
            
            if not words:
                return default_words
                
            return words
        except:
            return default_words
    
    def start_game(self, game_data=None):
        """Inicia o reinicia el juego"""
        messagebox.showinfo("Game", "Game starting...")
        
        # Reiniciar las variables del juego
        word_list = self.get_word_list()
        self.secret_word = random.choice(word_list).lower()
        self.guessed = ["_" for _ in self.secret_word]
        self.wrong_letters = []
        self.attempts_left = self.max_attempts
        self.game_over = False
        self.points = 0
        
        # Actualizar la interfaz
        self.word_var.set(" ".join(self.guessed))
        self.attempts_var.set(f"Attempts left: {self.attempts_left}")
        self.wrong_var.set("Wrong letters: ")
        self.points_var.set(f"Points: {self.points}")
        self.message_var.set("New game started! Guess a letter.")
        
        # Actualizar el dibujo del ahorcado
        self.hangman_drawing.config(state="normal")
        self.hangman_drawing.delete("1.0", "end")
        self.hangman_drawing.insert("1.0", self.get_hangman_drawing(0))
        self.hangman_drawing.config(state="disabled")
        
        # Habilitar el campo de entrada
        self.letter_entry.config(state="normal")
        self.letter_entry.delete(0, 'end')
        self.letter_entry.focus_set()
    
    def guess_letter(self, letter):
        """Procesa la letra ingresada por el usuario"""
        letter = letter.lower()
        
        if self.game_over:
            return
        
        # Validar que se ingrese una sola letra alfabética
        if not letter.isalpha() or len(letter) != 1:
            self.message_var.set("Please enter a valid letter.")
            return
        
        # Verificar si la letra ya ha sido utilizada
        if letter in self.guessed or letter in self.wrong_letters:
            self.message_var.set("You already tried that letter.")
            return
        
        # Procesar la letra
        letter_found = False
        for i, char in enumerate(self.secret_word):
            if char == letter:
                if self.guessed[i] == "_":  # Solo actualizar si no se ha revelado
                    self.guessed[i] = letter
                    if not letter_found:
                        self.points += 20  # Añadir puntos una vez por letra
                        letter_found = True
        
        if not letter_found:
            self.points -= 10
            self.attempts_left -= 1
            self.wrong_letters.append(letter)
            self.message_var.set("Incorrect letter.")
        else:
            self.message_var.set("Good!")
        
        # Actualizar la interfaz
        self.update_ui()
        
        # Verificar condiciones de victoria o derrota
        if "_" not in self.guessed:
            self.message_var.set("Congratulations, you won!")
            self.game_over = True
            self.handle_game_over()
        
        if self.attempts_left <= 0:
            self.message_var.set(f"You lost. The word was '{self.secret_word}'.")
            self.guessed = list(self.secret_word)
            self.game_over = True
            self.handle_game_over()
    
    def update_ui(self):
        """Actualiza la interfaz con el estado actual del juego"""
        self.word_var.set(" ".join(self.guessed))
        self.attempts_var.set(f"Attempts left: {self.attempts_left}")
        self.wrong_var.set(f"Wrong letters: {', '.join(self.wrong_letters)}")
        self.points_var.set(f"Points: {self.points}")
        
        # Actualizar el dibujo del ahorcado
        self.update_hangman_drawing(len(self.wrong_letters))
    
    def update_hangman_drawing(self, errors):
        """Actualiza el dibujo del ahorcado según los errores"""
        self.hangman_drawing.config(state="normal")
        self.hangman_drawing.delete("1.0", "end")
        self.hangman_drawing.insert("1.0", self.get_hangman_drawing(errors))
        self.hangman_drawing.config(state="disabled")
    
    def on_guess(self):
        """Maneja el intento de adivinar una letra"""
        if self.game_over:
            messagebox.showinfo("Game Over", "The game is over. Start a new game.")
            return
            
        letter = self.letter_entry.get().strip().lower()
        self.letter_entry.delete(0, 'end')
        
        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid input", "Please enter a single letter")
            return
        
        # Procesar la letra
        self.guess_letter(letter)
    
    def handle_game_over(self):
        """Maneja el fin del juego"""
        self.letter_entry.config(state="disabled")
        messagebox.showinfo("Game Over", f"{self.message_var.get()}\nYour score: {self.points}")
    
    def back_to_menu(self):
        """Vuelve al menú principal"""
        self.controller.show_frame("MainMenuScreen")
    
    def process_game_data(self, game_data):
        """Método para mantener compatibilidad con la interfaz original"""
        # Este método ya no es necesario ya que toda la lógica está integrada,
        # pero lo mantenemos para compatibilidad con el código existente
        pass
