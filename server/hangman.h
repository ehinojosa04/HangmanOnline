#ifndef HANGMAN_H
#define HANGMAN_H

#include <stdbool.h>

#define MAX_WORD_LENGTH 32
#define MAX_PLAYERS 4       // Ajustado al máximo de jugadores por sala
#define MAX_ATTEMPTS 6      // Intentos antes de perder
#define MAX_WRONG_LETTERS 9 // Letras incorrectas permitidas

typedef struct {
    char secret_word[MAX_WORD_LENGTH];  // Palabra a adivinar
    char guessed_letters[MAX_WORD_LENGTH]; // Letras adivinadas (ej: "p _ _ t _ n")
    char wrong_letters[MAX_WRONG_LETTERS + 1]; // Letras incorrectas (ej: "xzq")
    int attempts_left;      // Intentos restantes
    bool game_over;         // ¿Terminó el juego?
    int player_points[MAX_PLAYERS]; // Puntos por jugador
} HangmanGame;

// Inicialización y selección de palabra
void getRandomWord(const char *filename, char *word);
void startHangmanGame(HangmanGame *game, const char *word);

// Lógica del juego
const char* processGuess(HangmanGame *game, int player_id, char letter);

// Estado del juego
void getGameStateMessage(HangmanGame *game, char *message);

#endif