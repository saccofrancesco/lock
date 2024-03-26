# Importing Libraries
import customtkinter as ctk
from colors.colors import color
import os
from PIL import Image

# Creating the password entry widget with the option to show or not the password
class PasswordEntry(ctk.CTkFrame):

    # Storing constants to use in class
    EYE_ICON_PATH: str = os.path.join('assets', 'icon', 'open-eye.png')
    EYE_ICON: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(EYE_ICON_PATH),
        dark_image=Image.open(EYE_ICON_PATH),
        size=(28, 14)
    )
    CLOSED_EYE_ICON_PATH: str = os.path.join('assets', 'icon', 'closed-eye.png')
    CLOSED_EYE_ICON: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(CLOSED_EYE_ICON_PATH),
        dark_image=Image.open(CLOSED_EYE_ICON_PATH),
        size=(28, 18)
    )
    BGCOLOR: str = color('nord3')
    HOVERBGCOLOR: str = color('nord2')

    def __init__(self, master: ctk.CTkFrame, placeholder_text: str) -> None:

        # Initializing the super class
        super().__init__(master, fg_color='transparent')

        # Saving vars values for scoped rendering
        self.show_password: bool = False

        # Creating and placing the entry
        self.entry: ctk.CTkEntry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder_text,
            show='●',
            font=('arial', 14),
            fg_color=color('nord0'),
            placeholder_text_color=color('nord4'))
        self.entry.pack(side=ctk.LEFT, padx=(0, 5), pady=0, fill=ctk.BOTH, expand=True)

        # Creating and placing the toggle button
        self.toggle: ctk.CTkButton = ctk.CTkButton(
            self,
            text='',
            command=self.toggle_password,
            image=self.EYE_ICON,
            fg_color=self.BGCOLOR,
            hover_color=self.HOVERBGCOLOR,
            width=45)
        self.toggle.pack(side=ctk.RIGHT, padx=(5, 0), pady=0, fill=ctk.BOTH)

    # Update function to change icon used
    def toggle_password(self) -> None:
        self.show_password: bool = not self.show_password
        if self.show_password:
            self.entry.configure(show='')
            self.toggle.configure(image=self.CLOSED_EYE_ICON)
        else:
            self.entry.configure(show='●')
            self.toggle.configure(image=self.EYE_ICON)
