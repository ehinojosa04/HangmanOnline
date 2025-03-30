# socket_client.py
import socket
import sys

BUFFER_SIZE = 2048

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.token = " "
        self.username = " "
        self.roomID = " "
        self.connected = False

    def connect(self):
        """Establish connection to the server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            return True, f"Connected to {self.host} at port {self.port}"
        except socket.error as e:
            self.connected = False
            return False, f"Connection error: {e}"

    def disconnect(self):
        """Close the connection"""
        if self.client_socket:
            self.client_socket.close()
            self.connected = False
        self.token = " "
        self.username = " "
        self.roomID = " "

    def send_command(self, command, username=" ", password=" ", roomID=" "):
        """
        Send a command to the server and return the response
        
        Args:
            command: The command to send (REGISTER, LOGIN, LOGOUT, CREATE, JOIN, EXIT)
            username: Username for authentication commands
            password: Password for authentication commands
            roomID: Room ID for room operations
            
        Returns:
            tuple: (success: bool, response: str)
        """
        if not self.connected:
            return False, "Not connected to server"
            
        try:
            # Prepare the message
            message = f"{command} {username} {password} {self.token} {roomID}"
            
            # Send the message
            self.client_socket.sendall(message.encode())
            
            # Get the response
            response = self.client_socket.recv(BUFFER_SIZE).decode(encoding='windows-1252')
            
            # Update internal state based on response
            if command == "LOGIN" and "FAILED" not in response:
                self.token = response.strip()
                self.username = username
                return True, f"Session initiated with token: {self.token}"
            elif command == "LOGOUT":
                self.token = " "
                self.username = " "
                return True, response
            elif command == "CREATE":
                self.roomID = response.strip()
                return True, response
            elif (command == "JOIN" and "FAILED" not in response) or (command == "EXIT" and "FAILED" not in response):
                self.roomID = roomID if command == "JOIN" else " "
                return True, response
            else:
                return "FAILED" not in response, response
                
        except socket.error as e:
            self.connected = False
            return False, f"Socket error: {e}"

    def get_auth_options(self):
        """Return available options when not authenticated"""
        return ["Sign in", "Log in", "Exit"]

    def get_session_options(self):
        """Return available options when authenticated"""
        return ["Log out", "Create Room", "Join Room", "Exit Room", "Close Program"]

    def is_authenticated(self):
        """Check if user is authenticated"""
        return self.token != " "

    def get_current_room(self):
        """Get current room ID"""
        return self.roomID

    def get_username(self):
        """Get current username"""
        return self.username
