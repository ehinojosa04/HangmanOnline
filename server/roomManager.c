#include "roomManager.h"
#include <string.h>

Room *createRoom(Room rooms[], int max_rooms, char *admin_username, char *ip){
    for (int i = 0; i < max_rooms; i++){
        if(rooms[i].status == -1){
            rooms[i].status = 0;
            rooms[i].n_users = 1;
            rooms[i].index = i; 

            strcpy(rooms[i].admin.username, admin_username);
            generateRandomCode(rooms[i].password);

            joinRoom(rooms, i, admin_username, ip);

            return &rooms[i];
        }
    }
    return NULL;
}

Room *joinRoom(Room rooms[], int index, char *username, char *ip){
    if (index < 0 || rooms[index].status == -1) {
        return NULL;
    }

    for (int i = 0; i < MAX_PLAYERS; i++){
        if (strlen(rooms[index].users[i].username) == 0) {
            Room *room = &rooms[index];
            strcpy(room -> users[i].username, username);
            strcpy(room -> users[i].ip, ip);
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

    if (strcmp(rooms[index].admin.username, username) == 0) {
        memset(&rooms[index], 0, sizeof(Room));
        rooms[index].status = -1;
        return 1;
    }

    for (int i = 0; i < MAX_PLAYERS; i++){
        if (strcmp(rooms[index].users[i].username, username) == 0) {
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
        printf("- %s\n", room -> users[i].username);
    }
}

Client *initClient(Client clients[]){
    for (int i = 0; i < MAX_PLAYERS * MAX_ROOMS; i++){
        if (clients[i].status == -1){
            Client *client = &clients[i];
            return client;
        }
    }
    return NULL;
}
