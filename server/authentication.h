#ifndef AUTHENTICATION_H
#define AUTHENTICATION_H

#include <stdio.h>
#include <sqlite3.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/sha.h> // For password hashing


int register_user(sqlite3 *db, const char *username, const char *password);
void hash_password(const char *password, char *hashed_output);


#endif // HANGMAN_H

