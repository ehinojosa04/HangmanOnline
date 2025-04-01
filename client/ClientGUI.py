import tkinter as tk
from tkinter import messagebox
from views.home import HomeScreen
from views.login import LoginScreen
from views.signup import SignupScreen
from views.about import AboutScreen
from views.hangmangame import HangmanGameScreen
from views.main_menu import MainMenuScreen
from views.room import RoomScreen

class GUIManager:
    def __init__(self, root, client_state):
        self.root = root
        self.client_state = client_state
        self.current_screen = None
        self.screens = {}
        
        # Configure root window
        self.root.title("Hangman Game Client")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Initialize all screens but don't pack them yet
        self.initialize_screens()
        
        # Start with the home screen
        self.show_screen("HomeScreen")
    
    def initialize_screens(self):
        """Initialize all screens but don't display them"""
        self.screens = {
            "HomeScreen": HomeScreen(self.root, self),
            "LoginScreen": LoginScreen(self.root, self),
            "SignupScreen": SignupScreen(self.root, self),
            "AboutScreen": AboutScreen(self.root, self),
            "HangmanGameScreen": HangmanGameScreen(self.root, self),
            "MainMenuScreen": MainMenuScreen(self.root, self),
            "RoomScreen": RoomScreen(self.root, self)
        }
    
    def show_screen(self, screen_name):
        """Show the specified screen and hide the current one"""
        if self.current_screen:
            self.current_screen.pack_forget()
        
        self.current_screen = self.screens[screen_name]
        self.current_screen.pack(fill=tk.BOTH, expand=True)
        
        # Update window title based on current screen
        screen_title = screen_name.replace("Screen", "")
        self.root.title(f"Hangman Game - {screen_title}")
        
        # Call the screen's on_show method if it exists
        if hasattr(self.current_screen, 'on_show'):
            self.current_screen.on_show()
    
    def get_client_state(self):
        """Return the client state object"""
        return self.client_state
    
    def show_error(self, message):
        """Show an error message dialog"""
        messagebox.showerror("Error", message)
    
    def show_info(self, message):
        """Show an information message dialog"""
        messagebox.showinfo("Information", message)
    
    def on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.client_state.is_connected():
                self.client_state.disconnect()
            self.root.destroy()
    
    def get_screen(self, screen_name):
        """Retrieve a screen instance by name."""
        return self.screens.get(screen_name, None)
