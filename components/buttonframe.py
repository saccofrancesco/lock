# Importing Libraries
import customtkinter as ctk
from colors.colors import color
from components.buttons import *


# Craeting the buttonframe blueprint
class ButtonFrame(ctk.CTkFrame):
    """
    A custom frame class that creates a frame containing several buttons using customtkinter.

    Attributes:
        master (ctk.CTk): The parent widget.
        width (int): The width of the button frame.
        height (int): The height of the button frame.
        buttons (list): A list of button instances added to the frame.
    """

    def __init__(self, master: ctk.CTk, width: int, height: int) -> None:
        """
        Initializes the ButtonFrame class with the provided master, width, and height.
        Creates and places buttons in a 3x2 grid.

        Args:
            master (ctk.CTk): The parent widget.
            width (int): The width of the button frame.
            height (int): The height of the button frame.
        """
        # Initializing the super class
        super().__init__(master, width=width, height=height, fg_color=color("nord1"))

        # Create 6 buttons
        self.buttons = [
            CreateButton(self),
            UpdateButton(self),
            DeleteButton(self),
            SearchByUrlServiceButton(self),
            SearchByEmailUsernameButton(self),
            ListPasswordButton(self),
        ]

        # Place buttons in a 3x2  grid and expand them to fill the entire frame
        for i, button in enumerate(self.buttons):
            row = i // 2
            col = i % 2
            button.customgrid(row, col, ctk.NSEW)

        # Configure row and column weights to make buttons expandable
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
