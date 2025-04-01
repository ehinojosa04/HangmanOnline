# views/room.py
import tkinter as tk
from tkinter import messagebox

class RoomScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        self.room_info = None
        
        self.room_label = tk.Label(self, text="", font=("Arial", 16))
        self.room_label.pack(pady=10)

        self.admin_label = tk.Label(self, text="", font=("Arial", 12))
        self.admin_label.pack(pady=5)

        self.users_label = tk.Label(self, text="", font=("Arial", 12))
        self.users_label.pack(pady=5)

        self.private_label = tk.Label(self, text="", font=("Arial", 12))
        self.private_label.pack(pady=5)

        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.room_name_label = tk.Label(self, text="Room Name: ", font=("Arial", 12))
        self.room_name_label.pack(pady=10)

        self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("MainMenuScreen"))
        self.back_button.pack(pady=10)


        self.start_game_button = tk.Button(self, text="Start Game", command=self.start_game)

    def update_ui(self, room_info):
        """Con manejo de campos faltantes"""
        if not room_info:
            return
            
        # Valores por defecto si faltan datos
        data = {
            "index": room_info.get("index", "N/A"),
            "admin": {"username": room_info.get("admin", {}).get("username", "N/A")},
            "users": room_info.get("users", []),
            "n_users": room_info.get("n_users", len(room_info.get("users", []))),
            "isPrivate": room_info.get("isPrivate", False),
            "status": room_info.get("status", 0)
        }
        
        # Actualizar UI
        self.room_label.config(text=f"Room ID: {data['index']}")
        self.admin_label.config(text=f"Admin: {data['admin']['username']}")
        self.users_label.config(text=f"Users: {data['n_users']}/4")
        self.private_label.config(text=f"Private: {'Yes' if data['isPrivate'] else 'No'}")
        self.status_label.config(text=f"Status: {'In Progress' if data['status'] else 'Waiting'}")
        
        # Mostrar botones según rol
        is_admin = self.client.username == data['admin']['username']
        self.start_game_button.pack() if is_admin else self.start_game_button.pack_forget()
        self.leave_button.pack() if not is_admin else self.leave_button.pack_forget()

    def refresh_room_data(self):
        """Obtiene y actualiza los datos de la sala"""
        room_info = self.client.get_room_data()
        if room_info:
            self.set_room_info(room_info)
        else:
            messagebox.showerror("Error", "Could not fetch room data")
        
    def set_room_info(self, room_info=None):
        """Maneja tanto datos directos como auto-consulta"""
        if room_info is None:
            success, room_info = self.client.get_room_info()
            if not success:
                messagebox.showerror("Error", room_info)
                return

        # Asegurar que `room_info` sea un diccionario antes de usar `.get()`
        if not isinstance(room_info, dict):
            messagebox.showerror("Error", f"Unexpected data format: {room_info}")
            return
        
        try:
            self.room_name_label.config(text=f"Room Name: {room_info.get('name', 'Unknown')}")
            self.update_ui(room_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update UI: {str(e)}")
            
    def start_game(self):
        messagebox.showinfo("Game", "Game starting...")
        self.controller.show_frame("HangmanGameScreen")


