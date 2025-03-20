#include "authentication.h"

int register_user(sqlite3 *db, const char *username, const char *password) {
    char hashed_password[65] = {0};
    hash_password(password, hashed_password);

    const char *sql = "INSERT INTO Users (Username, PasswordHash) VALUES (?, ?);";
    sqlite3_stmt *stmt;
    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);

    if (rc != SQLITE_OK) {
        printf("Failed to prepare statement.\n");
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, hashed_password, -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    sqlite3_finalize(stmt);

    return rc == SQLITE_DONE;
}

int authenticate_user(sqlite3 *db, const char *username, const char *password) {
    char hashed_password[65] = {0};
    hash_password(password, hashed_password);

    const char *sql = "SELECT PasswordHash FROM Users WHERE Username = ?;";
    sqlite3_stmt *stmt;
    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);

    if (rc != SQLITE_OK) {
        printf("Failed to prepare statement.\n");
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        const char *stored_hash = (const char *)sqlite3_column_text(stmt, 0);
        if (strcmp(stored_hash, hashed_password) == 0) {
            printf("Login successful!\n");
            sqlite3_finalize(stmt);
            return 1;
        }
    }

    printf("Invalid username or password.\n");
    sqlite3_finalize(stmt);
    return 0;
}


void hash_password(const char *password, char *hashed_output) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char *)password, strlen(password), hash);

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf(hashed_output + (i * 2), "%02x", hash[i]); // Convert to hex string
    }
}


