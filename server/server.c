#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <signal.h>
#include <sqlite3.h>
#include <arpa/inet.h>

#include <sys/ipc.h>
#include <sys/shm.h>


#include "hangman.h"
#include "authentication.h"
#include "roomManager.h"

#define IP "127.0.0.1"

#define DATABASE "auth.db"
#define TOKEN_SIZE 65

#define CODE_SIZE 4
#define ROOM_CODE_CHARSET "ABCDEF1234567890"

int tcp_sd;
int udp_sd;

int PORT;

int rooms_shmid;
int clients_shmid;

Room *rooms;
Room *room;

Client *clients;
Client *client;


int room_count = 0;

void aborta_handler(int sig) {
    printf(".... Shutting down server (signal %d)\n", sig);
    close(tcp_sd);
    close(udp_sd);
    exit(0);
}

int send_udp_message(const char *hostname, int port, const char *message, size_t message_len) {
    int sockfd;
    struct sockaddr_in server_addr;
    
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        return -1;
    }
    
    memset(&server_addr, 0, sizeof(server_addr));
    
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    
    if (inet_pton(AF_INET, hostname, &server_addr.sin_addr) <= 0) {
        perror("invalid address/address not supported");
        close(sockfd);
        return -1;
    }
    
    ssize_t bytes_sent = sendto(sockfd, message, message_len, 0, (const struct sockaddr *)&server_addr, sizeof(server_addr));
    
    if (bytes_sent < 0) {
        perror("sendto failed");
        close(sockfd);
        return -1;
    }
    
    printf("Sent %zd bytes to %s:%d\n", bytes_sent, hostname, port);
    
    close(sockfd);
    return 0;
}


void handle_client(int client_sd) {
    client = initClient(clients);

    struct sockaddr_in client_addr;
    socklen_t addr_len = sizeof(client_addr);

    getpeername(client_sd, (struct sockaddr *)&client_addr, &addr_len);
    char client_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);

    strcpy(client -> ip,client_ip);
    client -> udp_port = PORT + 1;

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
            client = initClient(clients, username);
            printf("Client %s memaddress: %p\n",username, client);
            if (authenticate_user(db, username, password)) {
                generate_token(token, TOKEN_SIZE);
                store_token(db, username, token);
                send(client_sd, token, strlen(token), 0);

            } else {
                send(client_sd, "FAILED\n", 6, 0);
            }
        } else if (strcmp(command, "LOGOUT") == 0) {
            invalidate_token(db, username);
            send(client_sd, "SUCCESS\n", 8, 0);
        } else if (strcmp(command, "CREATE") == 0) { 
            room = createRoom(rooms, MAX_ROOMS, username, client_ip);
            if (room != NULL){
                printf("New room created successfuly in: %d\n", room->index);
                printPlayers(room);
                room_count++;

                char index[16];
                int len = sprintf(index, "%d", room->index);
                send(client_sd, index, len, 0);
            }
            else{
                send(client_sd, "FAILED\n", 6, 0);
            }
        }else if (strcmp(command, "JOIN") == 0) {
            room = joinRoom(rooms, atoi(roomID), username, client_ip);
            if (room != NULL){
                printf("User %s has joined room %d successfuly\n", username, room->index);
                printPlayers(room);

                char udp_msg[256];
                sprintf(udp_msg, "Player %s has joined the room %s\n", username, roomID);

                for (int i = 0; i < MAX_PLAYERS; i++) {
                    if (room->users[i].username[0] != '\0') {
                        printf("Sending update to player %s\n", room->users[i].username);
                            printf("message: '%s'", udp_msg);

                    if (send_udp_message(client_ip, PORT+1, udp_msg, strlen(udp_msg)) < 0) {
                        printf("Failed to send UDP update to player\n");
                    }
                }
            }

                send(client_sd, "SUCCESS\n", 8, 0);
            } else {
                send(client_sd, "FAILED\n", 6, 0);
            }
            
        } else if (strcmp(command, "EXIT") == 0) {
            if (exitRoom(rooms, atoi(roomID), username)){
                printf("User %s has successfuly left room %s", username, roomID);
                printPlayers(room);
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

int main(int argc, char *argv[]) {

    if (argc < 2) {
        printf("Usage: %s <PORT>\n", argv[0]);
        return 1;
    }

    PORT = atoi(argv[1]);

    srand(time(NULL));

    rooms_shmid = shmget(IPC_PRIVATE, sizeof(Room) * MAX_ROOMS, IPC_CREAT | 0666);
    if (rooms_shmid == -1) {
        perror("shmget");
        exit(1);
    }

    rooms = (Room *)shmat(rooms_shmid, NULL, 0);
    if (rooms == (void *)-1) {
        perror("shmat");
        exit(1);
    }

    for (int i = 0; i < MAX_ROOMS; i++){
        rooms[i].status = -1;
    }

    clients_shmid = shmget(IPC_PRIVATE, sizeof(Client) * MAX_ROOMS * MAX_PLAYERS, IPC_CREAT | 0666);
    if (clients_shmid == -1) {
        perror("shmget");
        exit(1);
    }

    clients = (Client *)shmat(clients_shmid, NULL, 0);
    if (clients == (void *)-1) {
        perror("shmat");
        exit(1);
    }

    for (int i = 0; i < MAX_ROOMS * MAX_PLAYERS; i++){
        strcpy(clients[i].username,"");
    }




    struct sockaddr_in sind, pin;
    socklen_t addrlen = sizeof(pin);

    if (signal(SIGINT, aborta_handler) == SIG_ERR) {
        perror("Could not set signal handler");
        return 1;
    }

    signal(SIGCHLD, SIG_IGN);

    if ((tcp_sd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("TCP socket");
        exit(1);
    }

    if ((udp_sd = socket(AF_INET, SOCK_DGRAM, 0)) == -1){
        perror("UDP socket");
        exit(1);
    }

    sind.sin_family = AF_INET;
    sind.sin_addr.s_addr = INADDR_ANY;
    sind.sin_port = htons(PORT);

    if (bind(tcp_sd, (struct sockaddr *)&sind, sizeof(sind)) == -1) {
        perror("bind");
        exit(1);
    }


    if (listen(tcp_sd, 5) == -1) {
        perror("listen");
        exit(1);
    }

    printf("IP ADDRESS: %s\nPort: %d\nListening...\n", IP, PORT);

    while (1) {
        int client_sd = accept(tcp_sd, (struct sockaddr *)&pin, &addrlen);
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
            close(tcp_sd);
            close(udp_sd);
            handle_client(client_sd);
        } else {
            close(client_sd);
        }
    }

    close(tcp_sd);
    close(udp_sd);
    return 0;
}

