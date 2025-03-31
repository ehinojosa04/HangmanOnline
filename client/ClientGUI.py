import tkinter as tk
from views.home import HomeScreen
from views.login import LoginScreen
from views.signup import SignupScreen
from views.about import AboutScreen
from views.hangmangame import HangmanGameScreen
from views.main_menu import MainMenuScreen  # Keep the import
from views.room import RoomScreen
from utils.SocketClient import SocketClient

class ClientGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Online App")
        self.geometry("800x800")
        
        self.client = SocketClient("127.0.0.1", 5000)
        self.client.connect()
        self.frames = {}
        
        # Initialize ONLY non-authenticated frames first
        for F in (HomeScreen, LoginScreen, SignupScreen, AboutScreen):
            page_name = F.__name__
            frame = F(self, self, self.client)
            print(f"[DEBUG] Initializing {page_name}, client ID: {id(frame.client)}")
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Initialize RoomScreen (if needed early)
        self.frames["RoomScreen"] = RoomScreen(self, self, self.client)
        self.frames["RoomScreen"].grid(row=0, column=0, sticky="nsew")
        
        # MainMenuScreen will be initialized AFTER login
        self.frames["MainMenuScreen"] = None  # Placeholder
        
        self.frames["HangmanGameScreen"] = HangmanGameScreen(self, self, self.client)
        self.frames["HangmanGameScreen"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeScreen")

    def init_main_menu(self):
        """Initialize MainMenuScreen only when needed"""
        if self.frames["MainMenuScreen"] is None:
            print("[DEBUG] Lazy-loading MainMenuScreen")
            self.frames["MainMenuScreen"] = MainMenuScreen(self, self, self.client)
            self.frames["MainMenuScreen"].grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name, **kwargs):
        # Lazy initialization for MainMenu
        if frame_name == "MainMenuScreen" and self.frames[frame_name] is None:
            self.init_main_menu()
        
        frame = self.frames[frame_name]
        
        if frame_name == "RoomScreen":
            frame.set_room_info(**kwargs)
        elif frame_name == "MainMenuScreen":
            frame.update_username()  # Force UI update
            
        frame.tkraise()

if __name__ == "__main__":
    app = ClientGUI()
    app.mainloop()