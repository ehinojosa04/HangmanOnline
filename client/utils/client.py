import socket
import sys


BUFFER_SIZE = 2048

def main():
    if len(sys.argv) != 3:
        print(f"Use: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    PORT = int(sys.argv[2])

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, PORT))
        print(f"Conected to {host} at port {PORT}\n")

        command = " "
        username = " "
        password = " "
        token = " "
        roomID = " "


        while True:
            options = []
            if token == " ":
                options = ["Sign in", "Log in", "Exit"]

                print("\nOptions")
                for idx,o in enumerate(options, start=1):
                    print(f"{idx}. {o}")

                option = input("Select an option: ")
                
                if option == "1":
                    command = "REGISTER"
                elif option == "2":
                    command = "LOGIN"
                elif option == "3":
                    print("Saliendo")
                    break
                else:
                    print("Invalid option")
                    continue

            elif roomID == " ":
                options = ["Log out", "Create Room", "Join Room", "Close Program"]

                print("\nOptions")
                for idx,o in enumerate(options, start=1):
                    print(f"{idx}. {o}")

                option = input("Select an option: ")
                
                if option == "1":
                    command = "LOGOUT"
                elif option == "2":
                    command = "CREATE"
                elif option == "3":
                    command = "JOIN"
                elif option == "4":
                    if roomID != " ":
                        command = "EXIT"
                    print("Exiting")
                    break
                else:
                    print("Invalid option")
                    continue

            else:
                options = ["Start Room", "Exit Room", "Close Program"]

                print("\nOptions")
                for idx,o in enumerate(options, start=1):
                    print(f"{idx}. {o}")

                option = input("Select an option: ")
                
                if option == "1":
                    command = "START"
                elif option == "2":
                    command = "EXIT"
                elif option == "3":
                    if roomID != " ":
                        command = "EXIT"
                    print("Exiting")
                    break
                else:
                    print("Invalid option")
                    continue

                

            if command in ["REGISTER", "LOGIN"]:
                username = input("User: ").strip()
                password = input("Password: ").strip()

            else:
                password = " "
                
                if command == "JOIN":
                    roomID = input("RoomID: ").strip()

            message = f"{command} {username} {password} {token} {roomID}"

            print(f"Message sent: '{command} {username} {password} {token} {roomID}'")
            client_socket.sendall(message.encode())

            response = client_socket.recv(BUFFER_SIZE).decode(encoding='windows-1252')
            print("Respuesta del servidor:", response)

            if command == "LOGIN" and "FAILED" not in response:
                token = response.strip()
                print(f"Session initiated with token: {token}")
            elif command == "LOGOUT":
                token = " "
            elif command == "CREATE":
                roomID = response.strip()
            elif (command == "JOIN" and "FAILED" in response) or (command == "EXIT" and "FAILED" not in response):
                roomID = " "

    except socket.error as e:
        print("Socket error:", e)

    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
