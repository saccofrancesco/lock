# Importing Libraries
import customtkinter as ctk
from colors.colors import color, darken_color
import os
from PIL import Image
from font.font import CustomFont
from components.toplevels import *

# Craeting the createbutton component
class CreateButton(ctk.CTkButton):

    # Storing constants to use in class
    PLUS_ICON_PATH: str = os.path.join('assets', 'icon', 'plus.png')
    PLUS_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(PLUS_ICON_PATH),
        dark_image=Image.open(PLUS_ICON_PATH),
        size=(25, 25)
    )
    BGCOLOR: str = color('nord14')
    TEXTCOLOR: str = color('nord2')

    def __init__(self, master: ctk.CTkFrame) -> None:

        # Initializing the super class
        super().__init__(
            master,
            text='Create Password',
            image=self.PLUS_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, 'normal'),
            anchor='center',
            text_color=self.TEXTCOLOR,
            command=self.open_top_level)
        
        # Storing toplevel window state
        self.toplevel_window = None
        
    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:

        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(10, 5), pady=(10, 5))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:

        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateTopLevel()  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

# Craeting the updatebutton component
class UpdateButton(ctk.CTkButton):

    # Storing constants to use in class
    ARROW_ICON_PATH: str = os.path.join('assets', 'icon', 'arrow.png')
    ARROW_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(ARROW_ICON_PATH),
        dark_image=Image.open(ARROW_ICON_PATH),
        size=(25, 25)
    )
    BGCOLOR: str = color('nord13')
    TEXTCOLOR: str = color('nord2')

    def __init__(self, master: ctk.CTkFrame) -> None:

        # Initializing the super class
        super().__init__(
            master,
            text='Update Password',
            image=self.ARROW_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, 'normal'),
            anchor='center',
            text_color=self.TEXTCOLOR,
            command=self.open_top_level)
        
        # Storing toplevel window state
        self.toplevel_window = None
        
    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:

        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(5, 10), pady=(10, 5))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:

        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = UpdateTopLevel()  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

# Craeting the deletebutton component
class DeleteButton(ctk.CTkButton):

    # Storing constants to use in class
    BIN_ICON_PATH: str = os.path.join('assets', 'icon', 'bin.png')
    BIN_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(BIN_ICON_PATH),
        dark_image=Image.open(BIN_ICON_PATH),
        size=(25, 25)
    )
    BGCOLOR: str = color('nord11')
    TEXTCOLOR: str = color('nord2')

    def __init__(self, master: ctk.CTkFrame) -> None:

        # Initializing the super class
        super().__init__(
            master,
            text='Delete Password',
            image=self.BIN_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, 'normal'),
            anchor='center',
            text_color=self.TEXTCOLOR,
            command=self.open_top_level)
        
        # Storing toplevel window state
        self.toplevel_window = None
        
    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:

        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(10, 5), pady=5)

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:

        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DeleteTopLevel()  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

# Craeting the searchbyurlbutton component
class SearchByUrlServiceButton(ctk.CTkButton):

    # Storing constants to use in class
    URL_ICON_PATH: str = os.path.join('assets', 'icon', 'url.png')
    URL_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(URL_ICON_PATH),
        dark_image=Image.open(URL_ICON_PATH),
        size=(25, 25)
    )
    BGCOLOR: str = color('nord8')
    TEXTCOLOR: str = color('nord2')

    def __init__(self, master: ctk.CTkFrame) -> None:

        # Initializing the super class
        super().__init__(
            master,
            text='by Url / Service',
            image=self.URL_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, 'normal'),
            anchor='center',
            text_color=self.TEXTCOLOR,
            command=self.open_top_level)
        
        # Storing toplevel window state
        self.toplevel_window = None
        
    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:

        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(5, 10), pady=5)
    
    # Function the corresponding toplevel window
    def open_top_level(self) -> None:

        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SearchTopLevel(('url', 'service'))  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

# Craeting the searchbyemailorusername component
class SearchByEmailUsernameButton(ctk.CTkButton):

    # Storing constants to use in class
    EMAIL_ICON_PATH: str = os.path.join('assets', 'icon', 'user.png')
    EMAIL_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(EMAIL_ICON_PATH),
        dark_image=Image.open(EMAIL_ICON_PATH),
        size=(25, 25)
    )
    BGCOLOR: str = color('nord4')
    TEXTCOLOR: str = color('nord2')

    def __init__(self, master: ctk.CTkFrame) -> None:

        # Initializing the super class
        super().__init__(
            master,
            text='by Email / User',
            image=self.EMAIL_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, 'normal'),
            anchor='center',
            text_color=self.TEXTCOLOR,
            command=self.open_top_level)
        
        # Storing toplevel window state
        self.toplevel_window = None
        
    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:

        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(10, 5), pady=(5, 10))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:

        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SearchTopLevel(('email', 'username'))  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

# Craeting the listpassword component
class ListPasswordButton(ctk.CTkButton):

    # Storing constants to use in class
    LIST_ICON_PATH: str = os.path.join('assets', 'icon', 'list.png')
    LIST_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(LIST_ICON_PATH),
        dark_image=Image.open(LIST_ICON_PATH),
        size=(25, 25)
    )
    BGCOLOR: str = color('nord15')
    TEXTCOLOR: str = color('nord2')

    def __init__(self, master: ctk.CTkFrame) -> None:

        # Initializing the super class
        super().__init__(
            master,
            text='List Passwords',
            image=self.LIST_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, 'normal'),
            anchor='center',
            text_color=self.TEXTCOLOR,
            command=self.open_top_level)
        
        # Storing toplevel window state
        self.toplevel_window = None
        
    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:

        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(5, 10), pady=(5, 10))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:

        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ListAllTopLevel()  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
