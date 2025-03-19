# Compiler and flags
CC = gcc
CFLAGS = -Wall
LDFLAGS = -lsqlite3 -lcrypto

# Output executable name
TARGET = server

# Object files
OBJ = server.o hangman.o authentication.o

# The default target to build the program
$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ) $(LDFLAGS)

# Compile server.o
server.o: server.c hangman.h authentication.h
	$(CC) $(CFLAGS) -c server.c

# Compile hangman.o
hangman.o: hangman.c hangman.h
	$(CC) $(CFLAGS) -c hangman.c

authentication.o: authentication.c authentication.h
	$(CC) $(CFLAGS) -c authentication.c

# Clean up object files and executable
clean:
	rm -f *.o $(TARGET)
