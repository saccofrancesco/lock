# Importing Libraries
import customtkinter as ctk
from colors.colors import color


# Creating the cancelbutton blueprint closing the toplevels
class CancellButton(ctk.CTkButton):
    """
    A custom button class for canceling and closing a top-level window.

    Attributes:
        BGCOLOR (str): Background color for the button.
        HOVERBGCOLOR (str): Background color for the button when hovered.
        TEXTCOLOR (str): Text color for the button.
    """

    # Storing constants to use in class
    BGCOLOR: str = color("nord3")
    HOVERBGCOLOR: str = color("nord2")
    TEXTCOLOR: str = color("nord4")

    def __init__(self, master: ctk.CTkFrame, window: ctk.CTkToplevel) -> None:
        """
        Initializes the CancellButton class with specific styles and properties.

        Args:
            master (ctk.CTkFrame): The parent frame.
            window (ctk.CTkToplevel): The top-level window to be closed.
        """
        super().__init__(
            master,
            text="Cancel",
            fg_color=self.BGCOLOR,
            text_color=self.TEXTCOLOR,
            hover_color=self.HOVERBGCOLOR,
            command=lambda: window.destroy(),
        )
