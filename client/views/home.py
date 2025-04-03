import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#e9e9e9")
        self.controller = controller
        
        # Contenedor centralizado
        container = tk.Frame(self, bg="#e9e9e9")
        container.pack(expand=True)

        # Canvas para dibujar el gallows y la figura del ahorcado
        canvas = tk.Canvas(container, width=150, height=200, bg="#e9e9e9", highlightthickness=0)
        canvas.pack(pady=(20, 10))
        
        # Dibujar el gallows y el ahorcado
        # Base
        canvas.create_line(20, 180, 130, 180, width=4, fill="#333333")
        # Poste vertical
        canvas.create_line(50, 180, 50, 20, width=4, fill="#333333")
        # Viga horizontal
        canvas.create_line(50, 20, 110, 20, width=4, fill="#333333")
        # Cuerda
        canvas.create_line(110, 20, 110, 40, width=4, fill="#333333")
        # Cabeza (círculo)
        canvas.create_oval(95, 40, 125, 70, width=4, outline="#333333")
        # Cuerpo
        canvas.create_line(110, 70, 110, 120, width=4, fill="#333333")
        # Brazo izquierdo
        canvas.create_line(110, 80, 80, 100, width=4, fill="#333333")
        # Brazo derecho
        canvas.create_line(110, 80, 140, 100, width=4, fill="#333333")
        # Pierna izquierda
        canvas.create_line(110, 120, 90, 150, width=4, fill="#333333")
        # Pierna derecha
        canvas.create_line(110, 120, 130, 150, width=4, fill="#333333")

        # Título principal
        title_label = tk.Label(
            container,
            text="Welcome to Hangman Online",
            font=("Arial", 20, "bold"),
            fg="#333333",
            bg="#e9e9e9"
        )
        title_label.pack(pady=(10, 20))

        # Configuración de estilo para botones
        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#ffffff",
            "fg": "#333333",
            "activebackground": "#d0d0d0",
            "width": 15,
            "relief": tk.RAISED,
            "bd": 2
        }

        # Lista de botones (texto y nombre de pantalla)
        buttons = [
            ("Log In", "LoginScreen"),
            ("Sign Up", "SignupScreen"),
            ("About", "AboutScreen"),
            ("Exit", None)
        ]

        for text, screen_name in buttons:
            if screen_name is None:
                cmd = self.controller.root.quit
            else:
                cmd = lambda name=screen_name: self.controller.show_screen(name)
            tk.Button(
                container,
                text=text,
                command=cmd,
                **button_style
            ).pack(pady=5)

        # Footer opcional
        footer = tk.Label(
            self,
            text="© 2026 Hangman Online",
            font=("Arial", 10),
            fg="#666666",
            bg="#e9e9e9"
        )
        footer.pack(side="bottom", pady=5) #cambios a esete pedo