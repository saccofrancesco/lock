# Importing Libraries
import customtkinter as ctk

# Creaeting the custom App font
class CustomFont(ctk.CTkFont):
    def __init__(self, size: int, weight: str) -> None:

        # Initializing the super class
        super().__init__('Impact', size, weight)
