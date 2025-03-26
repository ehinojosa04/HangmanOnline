#include "hangman.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int countLines(char *filename);
void getRandomWord(char *filename, char *dir);
void updateGameState(int *errorCount, char *word, char *guessedWord, char guess, char *errors);

void getRandomWord(char *filename, char *dir) {
    srand(time(NULL));
    FILE *fptr;
    fptr = fopen(filename, "r");
    
    if (fptr == NULL) {
        printf("Error opening file %s\n", filename);
        return;
    }
    
    int count = 0;
    int objective = rand() % countLines(filename);
    char word[32];
    
    while (fgets(word, sizeof(word), fptr)) {
        if (count == objective) {
            size_t len = strlen(word);
            if (len > 0 && word[len-1] == '\n') {
                word[len-1] = '\0';
            }
            break;
        } else {
            count++;
        }
    }
    
    strncpy(dir, word, strlen(word) + 1);
    fclose(fptr);
}

int countLines(char *filename) {
    FILE *fptr;
    fptr = fopen(filename, "r");
    
    if (fptr == NULL) {
        printf("Error opening file %s\n", filename);
        return 0;
    }
    
    char ch;
    int lines = 0;
    
    while ((ch = fgetc(fptr)) != EOF) {
        if (ch == '\n') {
            lines++;
        }
    }
    
    fclose(fptr);
    return lines;
}

// Function to update the game state with each guess
void updateGameState(int *errorCount, char *word, char *guessedWord, char guess, char *errors) {
    int correctGuess = 0;
    
    // Check if the guess is correct
    for (int i = 0; i < strlen(word); i++) {
        if (word[i] == guess) {
            guessedWord[i] = guess;
            correctGuess = 1;
        }
    }

    // If the guess is incorrect, update the error count and store the wrong guess
    if (!correctGuess) {
        errors[*errorCount] = guess;
        (*errorCount)++;
    }
}
