import socket
import sys

PUERTO = 5000
BUFFER_SIZE = 2048

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <host>")
        sys.exit(1)

    host = sys.argv[1]
    #message = sys.argv[2]

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((host, PUERTO))
        print(f"Conectado a {host} en el puerto {PUERTO}\n")
        print(f"Ingresa tu usuario: ")
        client_socket.sendall(message.encode())

        response = client_socket.recv(BUFFER_SIZE).decode()
        print("\nSe recibio:\n\n", response)

    except socket.error as e:
        print("Error de socket:", e)

    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()


