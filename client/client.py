import socket
import sys

PUERTO = 5000
BUFFER_SIZE = 2048

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <host>")
        sys.exit(1)

    host = sys.argv[1]

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, PUERTO))
        print(f"Conectado a {host} en el puerto {PUERTO}\n")

        command = " "
        username = " "
        password = " "
        token = " "
        roomID = " "


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
                options = ["Log out", "Create Room", "Join Room","Exit"]

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

            response = client_socket.recv(BUFFER_SIZE).decode()
            print("Respuesta del servidor:", response)

            if command == "LOGIN" and "Login failed" not in response:
                token = response.strip()
                print(f"Sesión iniciada con token: {token}")
            elif command == "LOGOUT":
                token = " "
            

    except socket.error as e:
        print("Error de socket:", e)

    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()

