# Importing Libraries
import customtkinter as ctk
from colors.colors import color

# Creating the cancelbutton blueprint closing the toplevels
class CancellButton(ctk.CTkButton):

    # Storing constants to use in class
    BGCOLOR: str = color('nord3')
    HOVERBGCOLOR: str = color('nord2')
    TEXTCOLOR: str = color('nord4')

    def __init__(self, master: ctk.CTkFrame, window: ctk.CTkToplevel) -> None:

        super().__init__(
            master,
            text='Cancel',
            fg_color=self.BGCOLOR,
            text_color=self.TEXTCOLOR,
            hover_color=self.HOVERBGCOLOR,
            command=lambda: window.destroy())
