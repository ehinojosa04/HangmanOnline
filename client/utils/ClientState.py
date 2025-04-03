import socket
import sys
import json

BUFFER_SIZE = 2048

class ClientState:
    def __init__(self, host, port):
        self.command = ""
        self.username = ""
        self.password = ""
        self.token = ""
        self.roomID = ""
        self.socket = None
        self.host = host
        self.port = port
        self.is_connected = False

        self.room_data = {}

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            print(f"Connected to {self.host} at port {self.port}\n")
            return True, "Connection successful"
        except socket.error as e:
            self.is_connected = False
            return False, f"Connection error: {e}"

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            self.is_connected = False
            print("Disconnected from server.")

    def send_command(self, command, **kwargs):
        """Send a command to the server with optional parameters."""
        if not self.is_connected or not self.socket:
            print("Client not connected.")
            return False, "Client not connected."

        # Prepare message
        username = kwargs.get("username", self.username)
        password = kwargs.get("password", self.password)
        token = kwargs.get("token", self.token)
        roomID = kwargs.get("roomID", self.roomID)

        message = f"{command} {username} {password} {token} {roomID}"
        print(f"Message sent: '{message}'")
        
        try:
            self.socket.sendall(message.encode())
            response = self.socket.recv(BUFFER_SIZE).decode(encoding='windows-1252')
            print("Response from server:", response)
        except socket.error as e:
            return False, f"Socket error: {e}"

        # Process server response
        print(f'command: {command}')
        print(f'response: {response}')
        if command == "LOGIN" and "FAILED" not in response:
            self.token = response.strip()
            print(f"Session initiated with token: {self.token}")
            return True, response
        elif command == "LOGOUT":
            self.token = ""
            return True, response
        elif command == "CREATE":
            self.roomID = response.strip()
            return True, response
        elif command == "JOIN" and "FAILED" in response:
            return False, response
        elif command == "EXIT" and "FAILED" not in response:
            self.roomID = ""
            return True, response
        elif "SUCCESS" in response:
            return True, response
        elif "GUESS_" in command and "FAILED" not in response:
            return True, response
        return False, response


    def handle_udp_message(self, decoded_message, room_screen=None, game_screen=None):
        try:
            room_data = json.loads(decoded_message)

            if room_data != self.room_data:  # Update only if there is a change
                self.room_data = room_data
                print("Updated room data:", room_data)

            # Update RoomScreen
                if room_screen:
                    room_screen.update_room_info()

            # Update HangmanGameScreen if the game is active
                #if game_screen and room_data.get("status") == "PLAYING":
                if game_screen:
                    game_screen.update_game_info()

        except json.JSONDecodeError:
            print("Failed to decode UDP message:", decoded_message)

