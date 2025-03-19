#ifndef HANGMAN_H
#define HANGMAN_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void getRandomWord(char *filename, char *dir);
int countLines(char *filename);

#endif

