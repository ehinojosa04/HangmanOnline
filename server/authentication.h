#ifndef AUTHENTICATION_H
#define AUTHENTICATION_H

#include <stdio.h>
#include <sqlite3.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/sha.h>
#include <openssl/rand.h>


int register_user(sqlite3 *db, const char *username, const char *password);
void hash_password(const char *password, char *hashed_output);
int authenticate_user(sqlite3 *db, const char *username, const char *password);

void generate_token(char *token, size_t length);
int store_token(sqlite3 *db, const char *username, const char *token);
int validate_token(sqlite3 *db, const char *username, const char *token);
int invalidate_token(sqlite3 *db, const char *username);

#endif // HANGMAN_H

