import socket
import sys

PORT = 5000
BUFFER_SIZE = 2048

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <host>")
        sys.exit(1)

    host = sys.argv[1]

    try:
        token = None
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, PORT))
        print(f"Connected to {host} on port {PORT}\n")

        while True:
            options = []
            if not token:
                options = ["Sign in", "Log in", "Exit"]

                print("\nOptions")
                for idx, o in enumerate(options, start=1):
                    print(f"{idx}. {o}")

                option = input("Choose an option: ")
                
                if option == "1":
                    command = "REGISTER"
                elif option == "2":
                    command = "LOGIN"
                elif option == "3":
                    print("Exiting")
                    break
                else:
                    print("Invalid option")
                    continue

            else:
                options = ["Log out", "Exit"]

                print("\nOptions")
                for idx, o in enumerate(options, start=1):
                    print(f"{idx}. {o}")

                option = input("Choose an option: ")
                
                if option == "1":
                    command = "LOGOUT"
                elif option == "2":
                    print("Exiting")
                    break
                else:
                    print("Invalid option")
                    continue

            if command in ["REGISTER", "LOGIN"]:
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                message = f"{command} {username} {password}"

            else:
                message = f"{command} {username}"

            print(f"Message sent: {message}")
            client_socket.sendall(message.encode())

            response = client_socket.recv(BUFFER_SIZE).decode()
            print("Server response:", response)

            if command == "LOGIN" and "Login failed" not in response:
                token = response.strip()
                print(f"Session started with token: {token}")
            elif command == "LOGOUT":
                token = None
            

    except socket.error as e:
        print("Socket error:", e)

    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()