#include "hangman.h"

int points = 0;

/*
int main() {
    int option;
    srand(time(NULL));
    
    printf("\n\nWelcome to Hangman!\n");
    
    do {
        printf("\n\nSelect an option: \n"
               "1 - Play\n"
               "2 - Add words\n"
               "3 - Exit\n\n");
        scanf("%d", &option);
        clearScreen();
        
        switch(option) {
            case 1:
                playGame();
                points = 0;
                break;
            case 2:
                addWords();
                break;
            case 3:
                printf("Thanks for playing! Come back soon!\n");
                break;
            default:
                printf("\nPlease enter a valid option\n");
        }
    } while(option != 3);
    
    return 0;
}

*/

void clearScreen() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

void playGame() {
    const char *filename = "words.txt";
    char word[MAX_WORD_LENGTH];
    char tempWord[MAX_WORD_LENGTH];
    char wrongLetters[MAX_ERRORS + 1] = {0};
    int errors = 0;
    bool letterFound;
    
    getRandomWord(filename, word);
    int wordLength = strlen(word);

    // Initialize temporary word with dashes
    for (int i = 0; i < wordLength; i++) {
        tempWord[i] = '-';
    }
    tempWord[wordLength] = '\0';

    printf("\n\n* Guess the word *\n");

    while (errors < MAX_ERRORS && strcmp(word, tempWord) != 0) {
        
        printf("\nMistakes: %d/%d\n", errors, MAX_ERRORS);
        if (errors > 0) {
            printf("Wrong letters: %s\n", wrongLetters);
        }
        printf("Word: %s\n", tempWord);
        printf("Points: %d\n", points);
        printf("Enter a letter: ");

        char guess;
        scanf(" %c", &guess);
        guess = tolower(guess);

        // Validate input
        if (!isalpha(guess)) {
            printf("Please enter only letters.\n");
            continue;
        }

        // Check if letter was already used
        bool alreadyUsed = false;

        // First check in correct letters (including first letter)
        for (int i = 0; i < wordLength; i++) {
            if (tolower(word[i]) == guess && tempWord[i] != '-') {
                alreadyUsed = true;
                break;
            }
        }

        // Then check in wrong letters
        if (!alreadyUsed) {
            for (int i = 0; i < errors; i++) {
                if (tolower(wrongLetters[i]) == guess) {
                    alreadyUsed = true;
                    break;
                }
            }
        }

        if (alreadyUsed) {
            printf("You already tried that letter!\n");
            continue;
        }
        
        // Search for letter in word (including first position)
        letterFound = false;
        for (int i = 0; i < wordLength; i++) {
            if (tolower(word[i]) == guess) {
                tempWord[i] = word[i]; // Keep original case
                if (!letterFound) { // Add points only once per letter
                    points += 20;
                    letterFound = true;
                }
            }
        }

        if (!letterFound) {
            points -= 10;
            wrongLetters[errors++] = guess;
            wrongLetters[errors] = '\0';
        }
    }

    // Show final result
    clearScreen();
    
    if (points < 0) points = 0;
    displayMessage(errors, word, points, wrongLetters);
}

void displayMessage(int errors, const char *word, int points, const char *wrongLetters) {
    if (errors == MAX_ERRORS) {
        printf("\nYou lost! The word was: %s\n", word);
        printf("Final score: %d\n", points);
        printf("Wrong letters: %s\n", wrongLetters);
    } else {
        printf("\nCongratulations! You won!\n");
        printf("Word: %s\n", word);
        printf("Score: %d\n", points);
        printf("Mistakes: %d\n", errors);
    }
}

int countLines(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file %s\n", filename);
        return 0;
    }
    
    int count = 0;
    char ch;
    while ((ch = fgetc(file)) != EOF) {
        if (ch == '\n') {
            count++;
        }
    }
    
    fclose(file);
    return count;
}

void getRandomWord(const char *filename, char *word) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file %s\n", filename);
        strcpy(word, "default");
        return;
    }
    
    int totalLines = countLines(filename);
    if (totalLines == 0) {
        strcpy(word, "default");
        fclose(file);
        return;
    }
    
    int targetLine = rand() % totalLines;
    int currentLine = 0;
    
    while (fgets(word, MAX_WORD_LENGTH, file)) {
        if (currentLine == targetLine) {
            // Remove any \r and \n
            size_t len = strlen(word);
            while (len > 0 && (word[len - 1] == '\n' || word[len - 1] == '\r')) {
                word[len - 1] = '\0';
                len--;
            }
            
            for (int i = 0; i < len; i++) {
                word[i] = tolower(word[i]);
            }
            break;
        }
        currentLine++;
    }
    
    fclose(file);
}

void addWords() {
    FILE *file = fopen("words.txt", "a+");
    if (file == NULL) {
        printf("Error opening words file\n");
        return;
    }
    
    char newWord[MAX_WORD_LENGTH];
    int continueAdding = 1;
    
    printf("\nCurrent words:\n");
    rewind(file);
    char word[MAX_WORD_LENGTH];
    int count = 0;
    while (fgets(word, MAX_WORD_LENGTH, file)) {
        word[strcspn(word, "\r\n")] = '\0';
        printf("%d. %s\n", ++count, word);
    }
    
    while (continueAdding) {
        printf("\nEnter a new word (letters only, max %d chars): ", MAX_WORD_LENGTH - 1);
        scanf("%s", newWord);
        
        // Validate length
        if (strlen(newWord) >= MAX_WORD_LENGTH) {
            printf("Word is too long. Maximum %d characters.\n", MAX_WORD_LENGTH - 1);
            continue;
        }
        
        // Convert to lowercase and validate characters
        bool valid = true;
        for (int i = 0; newWord[i]; i++) {
            if (!isalpha(newWord[i])) {
                valid = false;
                break;
            }
            newWord[i] = tolower(newWord[i]);
        }
        
        if (!valid) {
            printf("Only A-Z letters are allowed.\n");
            continue;
        }
        
        // Check if word already exists
        bool exists = false;
        rewind(file);
        while (fgets(word, MAX_WORD_LENGTH, file)) {
            word[strcspn(word, "\r\n")] = '\0';
            if (strcmp(word, newWord) == 0) {
                exists = true;
                break;
            }
        }
        
        if (exists) {
            printf("Word '%s' already exists in the list.\n", newWord);
        } else {
            fprintf(file, "%s\n", newWord);
            printf("Word '%s' added successfully.\n", newWord);
        }
        
        printf("\nAdd another word?\n1 - Yes\n0 - No\n");
        scanf("%d", &continueAdding);
    }
    
    fclose(file);
}
