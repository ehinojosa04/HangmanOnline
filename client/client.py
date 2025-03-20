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

        while True:
            print("\nOpciones:")
            print("1. Registrar")
            print("2. Iniciar sesión")
            print("3. Cerrar sesión")
            print("4. Salir")

            opcion = input("Elige una opción: ")

            if opcion == "1":
                command = "REGISTER"
            elif opcion == "2":
                command = "LOGIN"
            elif opcion == "3":
                command = "LOGOUT"
            elif opcion == "4":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
                continue

            if command in ["REGISTER", "LOGIN"]:
                username = input("Usuario: ").strip()
                password = input("Contraseña: ").strip()
                message = f"{command} {username} {password}"
            else:
                message = "LOGOUT"

            client_socket.sendall(message.encode())

            response = client_socket.recv(BUFFER_SIZE).decode()
            print("Respuesta del servidor:", response)

    except socket.error as e:
        print("Error de socket:", e)

    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()

