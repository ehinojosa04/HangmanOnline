#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <signal.h>
#include <unistd.h>

#include "hangman.h"
#include "authentication.h"

#define  IP    "127.0.0.1"
#define  PORT  5000
#define  DATABASE "auth.db"

int                  sd, sd_actual;  /* descriptores de sockets */
int                  addrlen;        /* longitud msgecciones */
struct sockaddr_in   sind, pin;      /* msgecciones sockets cliente u servidor */

void aborta_handler(int sig){
   printf("....abortando el proceso servidor %d\n",sig);
   close(sd);  
   close(sd_actual); 
   exit(1);
}

int main(){
    char msg[256];
    char msg_back[256];
    int sent;

    if (signal(SIGINT, aborta_handler) == SIG_ERR){
   	    perror("Could not set signal handler");
        return 1;
    }

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

    printf("IP ADDRESS: %s\nPuerto: %d\nEscuchando...\n", IP, PORT);
    
    if ((sd_actual = accept(sd, (struct sockaddr *)&pin, &addrlen)) == -1) {
		perror("accept");
		exit(1);
	}

        sqlite3 *db;
    if (sqlite3_open(DATABASE, &db)) {
        printf("Cannot open database: %s\n", sqlite3_errmsg(db));
        exit(1);
    }
    
    while (1) {
        int received = recv(sd_actual, msg, sizeof(msg) - 1, 0);
        if (received <= 0) {
            printf("Client disconnected.\n");
            break;
        }

        msg[received] = '\0';
        printf("Received: %s\n", msg);

        char command[16], username[32], password[32];
        if (sscanf(msg, "%s %s %s", command, username, password) < 2) {
            send(sd_actual, "Invalid command\n", 16, 0);
            continue;
        }

        if (strcmp(command, "REGISTER") == 0) {
            register_user(db, username, password);
            send(sd_actual, "User registered\n", 16, 0);
        } 
        else if (strcmp(command, "LOGIN") == 0) {
            if (authenticate_user(db, username, password)) {
                send(sd_actual, "Login successful\n", 18, 0);
            } else {
                send(sd_actual, "Login failed\n", 13, 0);
            }
        } 
        else if (strcmp(command, "LOGOUT") == 0) {
            send(sd_actual, "Logged out\n", 11, 0);
        } 
        else {
            send(sd_actual, "Unknown command\n", 17, 0);
        }
    }

    close(sd_actual);
    close(sd);
    sqlite3_close(db);
    printf("Server shutting down...\n");
    return 0;
}
