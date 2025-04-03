import tkinter as tk
import sys
import threading
import socket

from ClientGUI import GUIManager
from utils.ClientState import ClientState

# UDP Listening Function
def listen_for_udp_messages(host, port, client, room_screen, game_screen):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))  # Bind to the same port or a separate one
    last_message = ""

    while True:
        try:
            message, _ = udp_socket.recvfrom(1024)  # Buffer size
            decoded_message = message.decode("utf-8")

            if decoded_message != last_message:
                last_message = decoded_message
                client.handle_udp_message(decoded_message, room_screen, game_screen)

        except Exception as e:
            print(f"Error in UDP listener: {e}")
            break

def main():
    if len(sys.argv) != 3:
        print("USE App.py <host> <port>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])

    udp_host = "0.0.0.0"

    root = tk.Tk()
    client = ClientState(host, port)

    try:
        client.connect()
        app = GUIManager(root, client)
        room_screen = app.get_screen("RoomScreen")
        game_screen = app.get_screen("HangmanGameScreen")

        # Start the UDP listener in a separate thread
        udp_thread = threading.Thread(target=listen_for_udp_messages, args=(udp_host, port+1, client, room_screen, game_screen), daemon=True)
        udp_thread.start()

        root.mainloop()
    except Exception as e:
        print(f"Failed to start application: {e}")
    finally:
        if client.is_connected:
            client.disconnect()

if __name__ == "__main__":
    main()

