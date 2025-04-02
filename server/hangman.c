#include "hangman.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <stdbool.h>

// Carga una palabra aleatoria desde un archivo (o usa palabras por defecto)
void getRandomWord(const char *filename, char *word) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        // Palabras por defecto si no hay archivo
        const char *default_words[] = {
            "python", "hangman", "computer", "programming",
            "keyboard", "developer", "challenge"
        };
        int count = sizeof(default_words) / sizeof(default_words[0]);
        strcpy(word, default_words[rand() % count]);
        return;
    }

    char buffer[MAX_WORD_LENGTH];
    int total_words = 0;
    char *words[100]; // Máximo 100 palabras en el archivo

    while (fgets(buffer, MAX_WORD_LENGTH, file) && total_words < 100) {
        buffer[strcspn(buffer, "\r\n")] = '\0'; // Eliminar saltos de línea
        if (strlen(buffer) >= 2) {
            words[total_words] = strdup(buffer);
            total_words++;
        }
    }
    fclose(file);

    if (total_words > 0) {
        strcpy(word, words[rand() % total_words]);
        // Liberar memoria
        for (int i = 0; i < total_words; i++) free(words[i]);
    } else {
        strcpy(word, "hangman"); // Palabra por defecto
    }
}

// Inicia un nuevo juego de ahorcado
void startHangmanGame(HangmanGame *game, const char *word) {
    strncpy(game->secret_word, word, MAX_WORD_LENGTH - 1);
    game->secret_word[MAX_WORD_LENGTH - 1] = '\0';

    // Inicializar letras adivinadas como "_____"
    size_t len = strlen(word);
    for (size_t i = 0; i < len; i++) {
        game->guessed_letters[i] = '_';
    }
    game->guessed_letters[len] = '\0';

    game->wrong_letters[0] = '\0';
    game->attempts_left = MAX_ATTEMPTS;
    game->game_over = false;

    // Resetear puntos de jugadores
    for (int i = 0; i < MAX_PLAYERS; i++) {
        game->player_points[i] = 0;
    }
}

// Procesa un intento de letra (para un jugador específico)
const char* processGuess(HangmanGame *game, int player_id, char letter) {
    if (game->game_over) return "GAME_OVER";

    letter = tolower(letter);
    

    // Verificar si la letra ya fue usada
    if (strchr(game->guessed_letters, letter) != NULL) return "ALREADY_GUESSED";
    if (strchr(game->wrong_letters, letter) != NULL) return "ALREADY_GUESSED";

    bool correct = false;

    // Verificar si la letra está en la palabra secreta
    for (int i = 0; game->secret_word[i]; i++) {
        if (tolower(game->secret_word[i]) == letter) {
            game->guessed_letters[i] = letter;
            correct = true;
        }
    }

    if (correct) {
        game->player_points[player_id] += 10; // Puntos por acierto
        // Verificar si ganó
        if (!strchr(game->guessed_letters, '_')) {
            game->game_over = true;
            return "WIN";
        }
        return "CORRECT";
    } else {
        // Agregar letra incorrecta
        size_t len = strlen(game->wrong_letters);
        if (len < MAX_WRONG_LETTERS) {
            game->wrong_letters[len] = letter;
            game->wrong_letters[len + 1] = '\0';
        }
        game->attempts_left--;
        game->player_points[player_id] -= 5; // Penalización por error

        if (game->attempts_left <= 0) {
            game->game_over = true;
            return "LOSE";
        }
        return "WRONG";
    }
}

// Genera un mensaje de estado para broadcast (UDP)
void getGameStateMessage(HangmanGame *game, char *message) {
    snprintf(message, 256, 
             "WORD: %s | WRONG: %s | ATTEMPTS: %d | GAME_OVER: %d",
             game->guessed_letters, 
             game->wrong_letters, 
             game->attempts_left,
             game->game_over);
}