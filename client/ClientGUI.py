# main.py
import tkinter as tk
from views.home import HomeScreen
from views.login import LoginScreen
from views.signup import SignupScreen
from views.about import AboutScreen
from views.main_menu import MainMenuScreen
from views.room import RoomScreen

from utils.SocketClient import SocketClient

class ClientGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Online App")
        self.geometry("620x420")
        
        self.client = SocketClient("127.0.0.1", 5000)
        self.client.connect()
        self.frames = {}
        
        # Initialize all frames
        for F in (HomeScreen, LoginScreen, SignupScreen, AboutScreen, MainMenuScreen, RoomScreen):
            page_name = F.__name__
            frame = F(self, self, self.client)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("HomeScreen")  # Show the Home screen initially

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = ClientGUI()
    app.mainloop()

