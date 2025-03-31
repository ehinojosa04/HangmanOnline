#include "roomManager.h"
#include <string.h>

Room *createRoom(Room rooms[], int max_rooms, Client *client){
    for (int i = 0; i < max_rooms; i++){
        if(rooms[i].status == -1){
            Room *room = &rooms[i];
            room -> status = 0;
            room -> n_users = 1;
            room -> index = i;
            room -> admin = client;

            generateRandomCode(rooms[i].password);

            joinRoom(rooms, i, client);

            return room;
        }
    }
    return NULL;
}

Room *joinRoom(Room rooms[], int index, Client *client){
    if (index < 0 || rooms[index].status == -1) {
        return NULL;
    }
    
    Room *room = &rooms[index];
    for (int i = 0; i < MAX_PLAYERS; i++){
        if (room -> users[i] == NULL) {
            room -> users[i] = client;
            room -> n_users++;
            return room;
        }
    }
    return NULL;
}


int exitRoom(Room rooms[], int index, char *username){
    if (index < 0 || rooms[index].status == -1) {
        return 0;
    }

    if (strcmp(rooms[index].admin -> username, username) == 0) {
        memset(&rooms[index], 0, sizeof(Room));
        rooms[index].status = -1;
        return 1;
    }

    for (int i = 0; i < MAX_PLAYERS; i++){
        if (strcmp(rooms[index].users[i] -> username, username) == 0) {
            memset(&rooms[index].users[i], 0, sizeof(Client));
            rooms[index].n_users--;
            return 1;
        }
    }
    return 0;
}

void generateRandomCode(char *code){
    for (int i = 0; i < CODE_SIZE; i++) {
        code[i] = CHARSET[rand() % (sizeof(CHARSET) - 1)];
    }
    code[CODE_SIZE] = '\0';
}

void printPlayers(Room *room){
    printf("Players in Room %d:\n", room -> index);
    for (int i = 0; i < MAX_PLAYERS; i++){
        if (room -> users[i] != NULL) printf("- %s\n", room -> users[i] -> username);
    }
    printf("All player printed.\n");
}

Client *initClient(Client clients[]){
    for (int i = 0; i < MAX_PLAYERS * MAX_ROOMS; i++){
        if (clients[i].status == -1){
            Client *client = &clients[i];
            client -> status = 0;

            printf("Client initialized in %p", client);
            return client;
        }
    }
    return NULL;
}
