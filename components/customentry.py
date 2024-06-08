# Importing Libraries
import customtkinter as ctk
from colors.colors import color

# Creating the entry blueprint with custom color
class CustomEntry(ctk.CTkEntry):
    """
    A custom entry field class with specified colors and placeholder text.

    Args:
        master (ctk.CTkFrame): The parent frame.
        placeholder_text (str): The placeholder text to display in the entry field.
    """
    def __init__(self, master: ctk.CTkFrame, placeholder_text: str) -> None:
        """
        Initializes the CustomEntry class with specific colors and placeholder text.

        Args:
            master (ctk.CTkFrame): The parent frame.
            placeholder_text (str): The placeholder text to display in the entry field.
        """
        # Initializing the super class
        super().__init__(master,
                         fg_color=color('nord0'),
                         placeholder_text_color=color('nord4'),
                         placeholder_text=placeholder_text)
