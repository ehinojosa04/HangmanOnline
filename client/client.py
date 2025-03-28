import socket
import sys


BUFFER_SIZE = 2048

def main():
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    PUERTO = int(sys.argv[2])

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, PUERTO))
        print(f"Conectado a {host} en el puerto {PUERTO}\n")

        command = " "
        username = " "
        password = " "
        token = " "
        roomID = " "
        current_room = None


        while True:
            options = []
            if token == " ":
                options = ["Sign in", "Log in", "Exit"]

                print("\nOpciones")
                for idx,o in enumerate(options, start=1):
                    print(f"{idx}. {o}")

                option = input("Elige una opcion: ")
                
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

            else:
                options = ["Log out", "Create Room", "Join Room","Exit Room", "Close Program"]

                print("\nOpciones")
                for idx,o in enumerate(options, start=1):
                    print(f"{idx}. {o}")

                option = input("Elige una opcion: ")
                
                if option == "1":
                    command = "LOGOUT"
                elif option == "2":
                    command = "CREATE"
                elif option == "3":
                    command = "JOIN"
                elif option == "4":
                    command = "EXIT"
                elif option == "5":
                    if roomID != " ":
                        command = "EXIT"
                    print("Saliendo")
                    break
                else:
                    print("Invalid option")
                    continue

            if command in ["REGISTER", "LOGIN"]:
                username = input("Usuario: ").strip()
                password = input("Contraseña: ").strip()

            else:
                password = " "
                
                if command == "JOIN":
                    roomID = input("RoomID: ")

            message = f"{command} {username} {password} {token} {roomID}"

            print(f"Mensaje enviado: '{command} {username} {password} {token} {roomID}'")
            client_socket.sendall(message.encode())

            response = client_socket.recv(BUFFER_SIZE).decode(encoding='windows-1252')
            print("Respuesta del servidor:", response)

            if command == "LOGIN" and "FAILED" not in response:
                token = response.strip()
                print(f"Sesión iniciada con token: {token}")
            elif command == "LOGOUT":
                token = " "
            elif command == "CREATE":
                RoomID = response.strip()
            elif (command == "JOIN" and "FAILED" in response) or (command == "EXIT" and "FAILED" not in response):
                RoomID = " "

    except socket.error as e:
        print("Error de socket:", e)

    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()

