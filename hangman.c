#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void getRandomWord(char *filename);
int countLines(char *filename);

void getRandomWord(char *filename){
    srand(time(NULL));
    FILE *fptr;
    fptr = fopen(filename,"r");

    int count = 0;
    int objective = rand() % (countLines(filename));
    char word[32];
    printf("Your random number is %d\n", objective);


    while (fgets(word, sizeof(word), fptr)){
        if (count == objective - 1){
            printf("Tu palabra random es: %s\n", word);
            break;
        } else {
            count++;
        }
    }
}

int countLines(char *filename){

    FILE *fptr;
    fptr = fopen(filename,"r");

    char ch;
    int lines = 0;

    while ((ch = fgetc(fptr)) != EOF){
        if (ch == '\n'){
            lines++;
        }
    }
    fclose(fptr);
    return lines - 1;
}
