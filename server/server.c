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

    char username[32];
    char password[32];

    int received = recv(sd_actual, username, sizeof(username) - 1, 0);
    if (received == -1) {
        perror("recv username");
        exit(1);
    }

    username[received] = '\0';
    printf("Received username: %s\n", username);

    received = recv(sd_actual, password, sizeof(password) - 1, 0);
    if (received == -1) {
        perror("recv password");
        exit(1);
    }

    password[received] = '\0';
    printf("Received password: %s\n", password);

    snprintf(msg_back, sizeof(msg_back), "Authentication received!");
    
    sqlite3 *db;
    int rc = sqlite3_open(DATABASE, &db);

    if (rc) {
        printf("Cannot open database: %s\n", sqlite3_errmsg(db));
    exit(1);
    }

    register_user(db, username, password);


    int sent;
	if ( sent = send(sd_actual, msg_back, strlen(msg_back), 0) == -1) {
		perror("send");
		exit(1);
	}

    close(sd_actual);  
    close(sd);
    printf("Conexion cerrada\n");
    return 0;
}
