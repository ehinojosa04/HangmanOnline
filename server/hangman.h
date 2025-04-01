#ifndef HANGMAN_H
#define HANGMAN_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <stdbool.h>

#define MAX_WORD_LENGTH 32
#define MAX_ERRORS 6

enum letter_status{
    WRONG = -1,
    UNATTEMPTED,
    CORRECT
};

typedef struct Word{
    char attempted_letters[26];
    
} Word;

// Main Functions
void playGame();
void addWords();
void clearScreen();

// Utility Functions
int countLines(const char *filename);
void getRandomWord(const char *filename, char *word);
void displayMessage(int errors, const char *word, int points, const char *wrongLetters);

#endif
