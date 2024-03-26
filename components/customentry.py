# Importing Libraries
import customtkinter as ctk
from colors.colors import color

# Creating the entry blueprint with custom color
class CustomEntry(ctk.CTkEntry):

    def __init__(self, master: ctk.CTkFrame, placeholder_text: str) -> None:

        # Initializing the super class
        super().__init__(master,
                         fg_color=color('nord0'),
                         placeholder_text_color=color('nord4'),
                         placeholder_text=placeholder_text)
