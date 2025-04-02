#include "roomManager.h"
#include <string.h>

#define MAX_UDP 512

Room *createRoom(Room rooms[], int max_rooms, Client *client) {
    printf("Attempting to create a room for %p %s\n", client, client->username);
    for (int i = 0; i < max_rooms; i++) {
        if(rooms[i].status == INACTIVE) {
            Room *room = &rooms[i];
            room->status = WAITING;
            room->n_users = 0;
            room->index = i;
            
            generateRandomCode(rooms[i].password);
            
            // Inicializar el juego aquí
            getRandomWord("words.txt", room->word);  // Nueva línea
            startHangmanGame(&room->game, room->word);  // Nueva línea
            
            Room *joined_room = joinRoom(rooms, i, client);
            
            if (joined_room != NULL) {
                joined_room->admin = client;
                printf("Admin set to %p %s\n", joined_room->admin, joined_room->admin->username);
            } 
            
            return joined_room;
        }
    }
    return NULL;
}

Room *joinRoom(Room rooms[], int index, Client *client){
    if (index < 0 || rooms[index].status != WAITING) {
        return NULL;
    }
    
    Room *room = &rooms[index];
    for (int i = 0; i < MAX_PLAYERS; i++){
        if (room -> users[i] == NULL) {
            room -> users[i] = client;
            room -> n_users++;

            client -> status = WAITING;
            return room;
        }
    }
    return NULL;
}


int exitRoom(Room rooms[], int index, char *username) {
    if (index < 0 || rooms[index].status == INACTIVE) {
        return 0;
    }

    if (strcmp(rooms[index].admin->username, username) == 0) {
        // Reiniciar el juego cuando el admin sale
        memset(&rooms[index].game, 0, sizeof(HangmanGame));  // Nueva línea
        memset(&rooms[index], 0, sizeof(Room));
        rooms[index].status = INACTIVE;
        return 1;
    }

    for (int i = 0; i < MAX_PLAYERS; i++) {
        if (rooms[index].users[i] && strcmp(rooms[index].users[i]->username, username) == 0) {
            rooms[index].users[i] = NULL;  // Cambiado de memset a NULL assignment
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
        if (clients[i].status == INACTIVE){
            Client *client = &clients[i];
            client -> status = 0;

            printf("Client initialized in %p", client);
            return client;
        }
    }
    return NULL;
}

/*
void getRoomMessage(Room *room, char message[]){
    if (room -> status == INACTIVE) strcpy(message, "INACTIVE\n");
    else if (room -> status == WAITING){
        sprintf(message, "WAITING,%s,%s,%s,%s\n", 
                room -> users[0] ? room -> users [0] ->username : "",
                room -> users[1] ? room -> users [1] ->username : "",
                room -> users[2] ? room -> users [2] ->username : "",
                room -> users[3] ? room -> users [3] ->username : ""
        );
    }
    else if (room -> status == ACTIVE){
        sprintf(message, "STATUS: PLAYING\nPLAYERS:%s,%s,%s,%s\nWORD: %s\n", 
                room -> users[0] ? room -> users [0] ->username : "",
                room -> users[1] ? room -> users [1] ->username : "",
                room -> users[2] ? room -> users [2] ->username : "",
                room -> users[3] ? room -> users [3] ->username : "",
                room -> word
        );
    }
}
*/

void getRoomMessage(Room *room, char message[]) {
    char users_json[128] = "[";
    int first = 1;

    // Construct JSON array of users
    for (int i = 0; i < 4; i++) {
        if (room->users[i]) {
            if (!first) strcat(users_json, ", ");
            char user_entry[32 + 10];
            snprintf(user_entry, sizeof(user_entry), "\"%s\"", room->users[i]->username);
            strcat(users_json, user_entry);
            first = 0;
        }
    }
    strcat(users_json, "]");

    char *roomStatus = (room->status == 1) ? "PLAYING" : "WAITING";

    // Format JSON message
    if (room->status == INACTIVE) {
        snprintf(message, MAX_UDP, "{\"status\": \"INACTIVE\"}");
    } else {
        snprintf(message, MAX_UDP, 
                "{\"index\": \"%d\",\"status\": \"%s\", \"admin\":\"%s\",\"players\": %s, \"word\": \"%s\"}", 
                room->index, 
                roomStatus,
                room->admin->username, 
                users_json, 
                room->word);
    }

    //printf("%s",message);
}
