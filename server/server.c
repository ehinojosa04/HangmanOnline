#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <signal.h>
#include <unistd.h>

#include "hangman.h"

#define  IP    "127.0.0.1"
#define  PORT  5000

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

    getRandomWord("words.txt", msg_back);


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
