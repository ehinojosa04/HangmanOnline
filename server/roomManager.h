#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <arpa/inet.h>
#include "hangman.h" 

#define CHARSET "ABCDEF1234567890"
#define CODE_SIZE 4
#define MAX_PLAYERS 4
#define MAX_ROOMS 100

enum status {
    INACTIVE = -1,
    WAITING,
    ACTIVE
};

typedef struct Client {
    int status;
    char username[32];
    char ip[INET_ADDRSTRLEN];
    int udp_port;

} Client;

typedef struct Room {
    int isPrivate;
    char password[4];
    
    Client *admin;
    Client *users[4]; 
    int n_users;

    int index;
    int status;
    char word[32];

    int turn;

    HangmanGame game; 
    
} Room;

Room *createRoom(Room rooms[], int max_rooms, Client *client);
void generateRandomCode(char *code);
Room *joinRoom(Room rooms[], int index, Client *client);
int exitRoom(Room rooms[], int index, char *username);

void printPlayers(Room *room);
void getRoomMessage(Room *room, char message[]);

Client *initClient(Client clients[]);
