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





void generate_token(char *token, size_t length) {
    const char *hex_chars = "0123456789abcdef";
    // Calculate correct buffer size (half of token length since each byte becomes 2 hex chars)
    size_t buffer_size = length / 2;
    unsigned char buffer[buffer_size];
    
    if (RAND_bytes(buffer, buffer_size) != 1) {
        fprintf(stderr, "Error generating random bytes\n");
        return;
    }
    
    for (size_t i = 0; i < buffer_size; i++) {
        token[i * 2] = hex_chars[(buffer[i] >> 4) & 0xF];
        token[i * 2 + 1] = hex_chars[buffer[i] & 0xF];
    }
    // Null terminate at the correct position (length, not length+1)
    token[length] = '\0';
}

int store_token(sqlite3 *db, const char *username, const char *token) {
    sqlite3_stmt *stmt;
    const char *sql = "INSERT INTO sessions (username, token) VALUES (?, ?) "
                     "ON CONFLICT(username) DO UPDATE SET token=?, created_at=CURRENT_TIMESTAMP;";
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Error preparing statement: %s\n", sqlite3_errmsg(db));
        return 0;
    }
    
    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, token, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, token, -1, SQLITE_STATIC);
    
    int result = (sqlite3_step(stmt) == SQLITE_DONE);
    sqlite3_finalize(stmt);
    
    if (!result) {
        fprintf(stderr, "Error storing token: %s\n", sqlite3_errmsg(db));
    }
    
    return result;
}

int validate_token(sqlite3 *db, const char *username, const char *token) {
    sqlite3_stmt *stmt;
    const char *sql = "SELECT COUNT(*) FROM sessions WHERE username=? AND token=?;";
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Error preparing statement: %s\n", sqlite3_errmsg(db));
        return 0;
    }
    
    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, token, -1, SQLITE_STATIC);
    
    int valid = 0;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        valid = sqlite3_column_int(stmt, 0);
    }
    
    sqlite3_finalize(stmt);
    return valid > 0;
}

int invalidate_token(sqlite3 *db, const char *username) {
    sqlite3_stmt *stmt;
    const char *sql = "DELETE FROM sessions WHERE username=?;";
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Error preparing statement: %s\n", sqlite3_errmsg(db));
        return 0;
    }
    
    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    
    int result = (sqlite3_step(stmt) == SQLITE_DONE);
    sqlite3_finalize(stmt);
    
    if (!result) {
        fprintf(stderr, "Error invalidating token: %s\n", sqlite3_errmsg(db));
    }
    
    return result;
}
