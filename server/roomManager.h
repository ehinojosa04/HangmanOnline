#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <arpa/inet.h>

#define CHARSET "ABCDEF1234567890"
#define CODE_SIZE 4
#define MAX_PLAYERS 4

typedef struct Client {
    char username[32];
    char ip[INET_ADDRSTRLEN];
    int udp_port;

} Client;

typedef struct Room {
    int isPrivate;
    char password[4];
    
    Client admin;
    Client users[4];
    int n_users;

    int index;
    int status;

    char word[32];
} Room;

Room *createRoom(Room rooms[], int max_rooms, char *admin_username, char *ip);
void generateRandomCode(char *code);
Room *joinRoom(Room rooms[], int index, char *username, char *ip);
int exitRoom(Room rooms[], int index, char *username);

void printPlayers(Room *room);
