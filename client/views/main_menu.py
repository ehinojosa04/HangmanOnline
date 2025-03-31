# views/main_menu.py
import tkinter as tk
from tkinter import messagebox, simpledialog

class MainMenuScreen(tk.Frame):
    def __init__(self, master, controller, client):
        super().__init__(master)
        self.controller = controller
        self.client = client
        
        # Title Label
        self.title_label = tk.Label(self, text=f"Welcome, {self.client.get_username()}", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Room Info Label
        self.room_label = tk.Label(self, text="")
        self.room_label.pack(pady=10)

        # Buttons
        self.create_room_button = tk.Button(self, text="Create Room", command=self.create_room)
        self.join_room_button = tk.Button(self, text="Join Room", command=self.join_room)
        self.enter_room_button = tk.Button(self, text="Enter Room", command=self.enter_room)
        self.logout_button = tk.Button(self, text="Log Out", command=self.logout)
        self.exit_button = tk.Button(self, text="Exit", command=master.quit)

        self.create_room_button.pack(pady=5)
        self.join_room_button.pack(pady=5)
        self.enter_room_button.pack(pady=5)
        self.logout_button.pack(pady=5)
        self.exit_button.pack(pady=5)

        self.update_username()
    def update_username(self):
        """Actualiza el nombre de usuario mostrado"""
        username = self.client.get_username()
        print(f"DEBUG: Current username from client: {username}")  # Para diagnóstico
        self.title_label.config(text=f"Welcome, {username if username else 'Guest'}")
    def update_ui(self):
        """Update UI elements dynamically."""
        username = self.client.get_username()
        room_id = self.client.get_current_room()

        self.title_label.config(text=f"Welcome, {username}")
        
        if room_id:
            self.room_label.config(text=f"Current Room: {room_id}")
            self.enter_room_button.pack(pady=5)
        else:
            self.room_label.config(text="Not in a room")
            self.enter_room_button.pack_forget()

    def create_room(self):
        success, response = self.client.send_command("CREATE")
        if success:
            room_id = response.strip()
            self.client.roomID = room_id  # Almacenar el ID de la sala
            
            # Esperar un breve momento antes de solicitar la info
            self.after(500, lambda: self.show_room_after_creation(room_id))
        else:
            messagebox.showerror("Error", f"Failed to create room: {response}")

    def show_room_after_creation(self, room_id):
        """Espera a que la sala esté lista antes de mostrar"""
        success, room_info = self.client.get_room_info(room_id)
        
        if success:
            self.controller.show_frame("RoomScreen", room_info=room_info)
        else:
            # Si falla, mostrar datos básicos
            self.controller.show_frame("RoomScreen", room_info={
                "index": room_id,
                "name": f"New Room {room_id}",
                "admin": {"username": self.client.username},
                "users": [self.client.username],
                "n_users": 1,
                "isPrivate": False,
                "status": 0
            })

    def join_room(self):
        room_id = simpledialog.askstring("Room ID", "Enter Room ID to join:")
        
        if room_id:
            print(f"[DEBUG] Attempting to join room: {room_id}")
            
            # Verificar formato del room_id (debe ser numérico según tu servidor)
            if not room_id.isdigit():
                messagebox.showerror("Error", "Room ID must be a number")
                return
                
            success, response = self.client.send_command(
                "JOIN", 
                username=self.client.username,  # Envía explícitamente el username
                roomID=room_id
            )
            
            if success:
                print(f"[DEBUG] Join successful. Server response: {response}")
                self.client.roomID = room_id
                
                # Obtener info actualizada de la sala
                success, room_info = self.client.get_room_info(room_id)
                if not success:
                    print(f"[DEBUG] Failed to get room info: {room_info}")
                    # Crear datos mínimos como fallback
                    room_info = {
                        "index": room_id,
                        "name": f"Room {room_id}",
                        "admin": {"username": "Unknown"},
                        "users": [self.client.username],
                        "n_users": 1,
                        "isPrivate": False,
                        "status": 0
                    }
                
                self.controller.show_frame("RoomScreen", room_info=room_info)
            else:
                messagebox.showerror("Error", 
                    f"Failed to join room {room_id}:\n{response}\n"
                    f"Possible reasons:\n"
                    f"- Room doesn't exist\n"
                    f"- Room is full\n"
                    f"- You're already in the room")
    def enter_room(self):
        # Obtener info de la sala
        room_info = self.get_room_info()  # Ahora esto devuelve directamente el diccionario
        
        if room_info:  # Siempre tendrá datos (incluso mock si falla)
            self.controller.show_frame("RoomScreen", room_info=room_info)
        else:
            messagebox.showerror("Error", "Could not get room information")
            
    def get_room_info(self):
        """Obtiene la información actual de la sala desde el servidor"""
        try:
            # Obtener datos básicos de la sala desde el cliente
            room_index = self.client.get_current_room()
            
            # Hacer una solicitud al servidor para obtener detalles completos
            success, room_data = self.client.get_room_info(room_index)
            
            if not success:
                print(f"Error getting room info: {room_data}")
                # Retornar datos mock como fallback
                return {
                    "index": self.client.get_current_room(),
                    "name": f"Sala {self.client.get_current_room()}",
                    "admin": {"username": self.client.username},
                    "users": [self.client.username],
                    "n_users": 1,
                    "isPrivate": False,
                    "status": 0,
                    "word_progress": "_ _ _ _ _",
                    "attempts_left": 6
                }
            
            # Construir el diccionario de información
            return {
                "index": room_index,
                "name": room_data.get("name", f"Sala {room_index}"),
                "admin": {
                    "username": room_data.get("admin", {}).get("username", self.client.username)
                },
                "users": room_data.get("users", []),
                "n_users": len(room_data.get("users", [])),
                "isPrivate": room_data.get("isPrivate", False),
                "status": room_data.get("status", 0),  # 0 = Waiting, 1 = In Game
                "word_progress": room_data.get("word_progress", ""),
                "attempts_left": room_data.get("attempts_left", 6)
            }
            
        except Exception as e:
            print(f"Error at obtain room data: {e}")
            # Retornar datos mock como fallback
            return {
                "index": self.client.get_current_room(),
                "name": f"Sala {self.client.get_current_room()}",
                "admin": {"username": self.client.username},
                "users": [self.client.username],
                "n_users": 1,
                "isPrivate": False,
                "status": 0,
                "word_progress": "_ _ _ _ _",
                "attempts_left": 6
            }

    def logout(self):
        success, response = self.client.send_command("LOGOUT")
        if success:
            messagebox.showinfo("Success", "You have logged out.")
            self.client.disconnect()
            self.controller.show_frame("HomeScreen")
        else:
            messagebox.showerror("Error", f"Logout failed: {response}")

