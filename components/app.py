# Importing Libraries
import customtkinter as ctk
from components.buttonframe import ButtonFrame
from components.header import Header
from colors.colors import color

# Craeting the App blueprint
class App(ctk.CTk):
    def __init__(self, title: str, size: tuple) -> None:

        # Initializing the super class
        super().__init__(fg_color=color('nord0'))
        self.resizable(False, False)

        # Configuring title and size
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

        # Placing the App header
        self.header: Header = Header(self)
        self.header.pack()

        # Creating and placing the buttonframe
        self.buttonframe: ButtonFrame = ButtonFrame(
            self, int(size[0]), int(size[1]))
        self.buttonframe.pack(after=self.header, fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.buttonframe.pack()

        # Running the App
        self.run()

    # Auxiliar method for running the App
    def run(self) -> None:
        self.mainloop()
