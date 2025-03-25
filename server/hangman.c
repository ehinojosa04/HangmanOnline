#include "hangman.h"

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
    
    printf("Your random number is %d\n", objective);
    
    while (fgets(word, sizeof(word), fptr)) {
        if (count == objective) {
            // Remove newline character if present
            size_t len = strlen(word);
            if (len > 0 && word[len-1] == '\n') {
                word[len-1] = '\0';
            }
            printf("Tu palabra random es: %s\n", word);
            break;
        } else {
            count++;
        }
    }
    
    // Copy the word to the destination, not the other way around
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
