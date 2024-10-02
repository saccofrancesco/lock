# Importing Libraries
import customtkinter as ctk


# Creaeting the custom App font
class CustomFont(ctk.CTkFont):
    """
    Represents a custom font for the application.

    This class inherits from ctk.CTkFont and allows creating custom fonts with specified size and weight.

    Args:
        size (int): The size of the font.
        weight (str): The weight of the font.

    Attributes:
        Inherits attributes from the parent class ctk.CTkFont.

    Note:
        The font family is set to 'Impact' by default.

    Example:
        Creating a custom font with size 12 and normal weight:

        custom_font = CustomFont(size=12, weight='normal')
    """

    def __init__(self, size: int, weight: str) -> None:
        """
        Initializes a CustomFont object with the specified size and weight.

        Args:
            size (int): The size of the font.
            weight (str): The weight of the font.
        """
        # Initializing the super class
        super().__init__("Impact", size, weight)
