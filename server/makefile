# Compiler and flags
CC = gcc
CFLAGS = -Wall

# Output executable name
TARGET = server

# Object files
OBJ = server.o hangman.o

# The default target to build the program
$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

# Compile server.o
server.o: server.c hangman.h
	$(CC) $(CFLAGS) -c server.c

# Compile hangman.o
hangman.o: hangman.c hangman.h
	$(CC) $(CFLAGS) -c hangman.c

# Clean up object files and executable
clean:
	rm -f *.o $(TARGET)
