#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <unistd.h>
#include <signal.h>
#include <sqlite3.h>

#include "hangman.h"
#include "authentication.h"

#define IP "127.0.0.1"
#define PORT 5000
#define DATABASE "auth.db"
#define TOKEN_SIZE 65

int sd; /* Server socket descriptor */

void aborta_handler(int sig) {
    printf(".... Shutting down server (signal %d)\n", sig);
    close(sd);
    exit(0);
}

void handle_client(int client_sd) {
    char msg[256];

    sqlite3 *db;
    if (sqlite3_open(DATABASE, &db)) {
        printf("Cannot open database: %s\n", sqlite3_errmsg(db));
        close(client_sd);
        exit(1);
    }

    while (1) {
        int received = recv(client_sd, msg, sizeof(msg) - 1, 0);
        if (received <= 0) {
            printf("Client disconnected.\n");
            break;
        }

        msg[received] = '\0';
        printf("Received: %s\n", msg);

        char token[TOKEN_SIZE];
        char command[16], username[32], password[32] = "", received_token[TOKEN_SIZE + 1] = "";
        int parsed_args = sscanf(msg, "%s %s %s %s", command, username, password, received_token);

        if (parsed_args < 2) {
            send(client_sd, "Invalid command\n", 16, 0);
            continue;
        }

        if (strcmp(command, "REGISTER") == 0) {
            if (register_user(db, username, password)) {
                send(client_sd, "User registered\n", 16, 0);
            } else {
                send(client_sd, "Unable to register user\n", 25, 0);
            }
        } else if (strcmp(command, "LOGIN") == 0) {
            if (authenticate_user(db, username, password)) {
                generate_token(token, TOKEN_SIZE);
                store_token(db, username, token);
                send(client_sd, token, TOKEN_SIZE, 0);
            } else {
                send(client_sd, "Login failed\n", 13, 0);
            }
        } else if (strcmp(command, "LOGOUT") == 0) {
            invalidate_token(db, username);
            send(client_sd, "Logged out\n", 11, 0);
        } else {
            send(client_sd, "Unknown command\n", 17, 0);
        }
    }

    close(client_sd);
    sqlite3_close(db);
    printf("Client handler process exiting...\n");
    exit(0);  // Ensure child process exits
}

int main() {
    struct sockaddr_in sind, pin;
    socklen_t addrlen = sizeof(pin);

    if (signal(SIGINT, aborta_handler) == SIG_ERR) {
        perror("Could not set signal handler");
        return 1;
    }

    signal(SIGCHLD, SIG_IGN);

    if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        exit(1);
    }

    sind.sin_family = AF_INET;
    sind.sin_addr.s_addr = INADDR_ANY;
    sind.sin_port = htons(PORT);

    if (bind(sd, (struct sockaddr *)&sind, sizeof(sind)) == -1) {
        perror("bind");
        exit(1);
    }

    if (listen(sd, 5) == -1) {
        perror("listen");
        exit(1);
    }

    printf("IP ADDRESS: %s\nPort: %d\nListening...\n", IP, PORT);

    while (1) {
        int client_sd = accept(sd, (struct sockaddr *)&pin, &addrlen);
        if (client_sd == -1) {
            perror("accept");
            continue;  // Don't exit; just retry
        }

        printf("New client connected\n");

        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            close(client_sd);
        } else if (pid == 0) {
            close(sd);
            handle_client(client_sd);
        } else {
            close(client_sd);
        }
    }

    close(sd);
    return 0;
}

