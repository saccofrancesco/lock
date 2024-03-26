# Importing Libraries
import customtkinter as ctk
import os
from PIL import Image

# Craeting the header blueprint
class Header(ctk.CTkFrame):

    # Storing constants to use in class
    BASE_PATH: str = 'assets'
    TITLE_PATH: str = os.path.join(BASE_PATH, 'img')
    DARK_TITLE_PATH: str = os.path.join(TITLE_PATH, 'dark-title.png')
    TEXT_IMG_SIZE: tuple[int, int] = (196, 50)

    def __init__(self, master: ctk.CTk) -> None:

        # Initializing the super class
        super().__init__(master, fg_color='transparent')

        # Placing the title
        text_img: ctk.CTkImage = ctk.CTkImage(
            Image.open(self.DARK_TITLE_PATH),
            Image.open(self.DARK_TITLE_PATH),
            self.TEXT_IMG_SIZE
        )

        # Insert the image in his label
        text_label: ctk.CTkLabel = ctk.CTkLabel(self, image=text_img, text='')

        # Placing the label
        text_label.pack(pady=(20, 10))
