#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <unistd.h>
#include <signal.h>
#include <sqlite3.h>

#include <sys/ipc.h>
#include <sys/shm.h>


#include "hangman.h"
#include "authentication.h"
#include "roomManager.h"

#define IP "127.0.0.1"
#define PORT 5000
#define DATABASE "auth.db"
#define TOKEN_SIZE 65

#define CODE_SIZE 4
#define ROOM_CODE_CHARSET "ABCDEF1234567890"
#define MAX_ROOMS 100

int sd; /* Server socket descriptor */

int shmid;
Room *rooms;

int room_count = 0;

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
        char command[16], username[32], password[32] = "", received_token[TOKEN_SIZE + 1] = "", roomID[CODE_SIZE] = "";
        int parsed_args = sscanf(msg, "%s %s %s %s %s", command, username, password, received_token, roomID);

        if (parsed_args < 2) {
            send(client_sd, "Invalid command\n", 16, 0);
            continue;
        }

        if (strcmp(command, "REGISTER") == 0) {
            if (register_user(db, username, password)) {
                send(client_sd, "User registered\n", 16, 0);
            } else {
                send(client_sd, "FAILED\n", 6, 0);
            }
        } else if (strcmp(command, "LOGIN") == 0) {
            if (authenticate_user(db, username, password)) {
                generate_token(token, TOKEN_SIZE);
                store_token(db, username, token);
                send(client_sd, token, TOKEN_SIZE, 0);

            } else {
                send(client_sd, "FAILED\n", 6, 0);
            }
        } else if (strcmp(command, "LOGOUT") == 0) {
            invalidate_token(db, username);
            send(client_sd, "SUCCESS\n", 8, 0);
        } else if (strcmp(command, "CREATE") == 0) {
            Room *newRoom; 
            newRoom = createRoom(rooms, MAX_ROOMS, username);
            if (newRoom != NULL){
                printf("New room created successfuly in: %d\n", newRoom->index);
                printPlayers(rooms, atoi(roomID));
                room_count++;

                char index[16];
                int len = sprintf(index, "%d", newRoom->index);
                send(client_sd, index, len, 0);
            }
            else{
                send(client_sd, "FAILED\n", 6, 0);
            }
        }else if (strcmp(command, "JOIN") == 0) {
            if (joinRoom(rooms,  atoi(roomID), username)){
                printf("User %s has joined room %s successfuly\n", username, roomID);
                printPlayers(rooms, atoi(roomID));
                
                send(client_sd, "SUCCESS\n", 8, 0);
            } else {
                send(client_sd, "FAILED\n", 6, 0);
            }
            
        } else if (strcmp(command, "EXIT") == 0) {
            if (exitRoom(rooms, atoi(roomID), username)){
                printf("User %s has successfuly left room %s", username, roomID);
                printPlayers(rooms, atoi(roomID));
                send(client_sd, "SUCCESS\n", 8, 0);
            } else {
                send(client_sd, "FAILED\n", 6, 0);
            }

        } else {
            send(client_sd, "Unknown command\n", 17, 0);
        }
    }

    close(client_sd);
    sqlite3_close(db);
    printf("Client handler process exiting...\n");
    exit(0);
}

int main() {
    srand(time(NULL));

    shmid = shmget(IPC_PRIVATE, sizeof(Room) * MAX_ROOMS, IPC_CREAT | 0666);
    if (shmid == -1) {
        perror("shmget");
        exit(1);
    }

    rooms = (Room *)shmat(shmid, NULL, 0);
    if (rooms == (void *)-1) {
        perror("shmat");
        exit(1);
    }

    for (int i = 0; i < MAX_ROOMS; i++){
        rooms[i].status = -1;
    }

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
            continue;
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

