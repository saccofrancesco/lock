# Importing Libraries
import customtkinter as ctk
import tkinter as tk
from components.buttonframe import ButtonFrame
from components.header import Header
from colors.colors import color
from utils.paths import resource_path


# Craeting the App blueprint
class App(ctk.CTk):
    """
    A custom application class that creates the main application window using customtkinter.

    Attributes:
        title (str): The title of the application window.
        size (tuple): The size of the application window (width, height).
        header (Header): The header component of the application.
        buttonframe (ButtonFrame): The button frame component of the application.
    """

    def __init__(self, title: str, size: tuple) -> None:
        """
        Initializes the App class with the provided title and size. Sets up the main window, header, and button frame.

        Args:
            title (str): The title of the application window.
            size (tuple): The size of the application window (width, height).
        """
        # Initializing the super class
        super().__init__(fg_color=color("nord0"))
        self.resizable(False, False)

        # Configuring title and size
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self._app_icon = None
        self._set_window_icon()

        # Placing the App header
        self.header: Header = Header(self)
        self.header.pack()

        # Creating and placing the buttonframe
        self.buttonframe: ButtonFrame = ButtonFrame(self, int(size[0]), int(size[1]))
        self.buttonframe.pack(
            after=self.header, fill=ctk.BOTH, expand=True, padx=10, pady=10
        )
        self.buttonframe.pack()

        # Running the App
        self.run()

    def _set_window_icon(self) -> None:
        """Set the window icon when available on the current platform."""
        try:
            self._app_icon = tk.PhotoImage(
                file=resource_path("assets", "icon", "logo.png")
            )
            self.iconphoto(True, self._app_icon)
        except tk.TclError:
            self._app_icon = None

    # Auxiliar method for running the App
    def run(self) -> None:
        """
        Starts the application's main event loop.
        """
        self.mainloop()
