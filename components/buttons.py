# Importing Libraries
import customtkinter as ctk
from colors.colors import color, darken_color
import os
from PIL import Image
from font.font import CustomFont
from components.toplevels import *


# Craeting the createbutton component
class CreateButton(ctk.CTkButton):
    """
    A custom button class for creating a password. It initializes with a plus icon and specific styles.

    Attributes:
        PLUS_ICON_PATH (str): Path to the plus icon image.
        PLUS_IMG (ctk.CTkImage): CustomTkinter image object for the plus icon.
        BGCOLOR (str): Background color for the button.
        TEXTCOLOR (str): Text color for the button.
    """

    # Storing constants to use in class
    PLUS_ICON_PATH: str = os.path.join("assets", "icon", "plus.png")
    PLUS_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(PLUS_ICON_PATH),
        dark_image=Image.open(PLUS_ICON_PATH),
        size=(25, 25),
    )
    BGCOLOR: str = color("nord14")
    TEXTCOLOR: str = color("nord2")

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes the CreateButton class with specific styles and properties.

        Args:
            master (ctk.CTkFrame): The parent frame.
        """
        # Initializing the super class
        super().__init__(
            master,
            text="Create Password",
            image=self.PLUS_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, "normal"),
            anchor="center",
            text_color=self.TEXTCOLOR,
            command=self.open_top_level,
        )

        # Storing toplevel window state
        self.toplevel_window = None

    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:
        """
        Custom method to place the button in the grid layout.

        Args:
            row (int): The row position in the grid.
            column (int): The column position in the grid.
            sticky (str): The sticky option for the grid.
        """
        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(10, 5), pady=(10, 5))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:
        """
        Opens the corresponding top-level window for creating a password.
        """
        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = (
                CreateTopLevel()
            )  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


# Craeting the updatebutton component
class UpdateButton(ctk.CTkButton):
    """
    A custom button class for updating a password. It initializes with an arrow icon and specific styles.

    Attributes:
        ARROW_ICON_PATH (str): Path to the arrow icon image.
        ARROW_IMG (ctk.CTkImage): CustomTkinter image object for the arrow icon.
        BGCOLOR (str): Background color for the button.
        TEXTCOLOR (str): Text color for the button.
    """

    # Storing constants to use in class
    ARROW_ICON_PATH: str = os.path.join("assets", "icon", "arrow.png")
    ARROW_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(ARROW_ICON_PATH),
        dark_image=Image.open(ARROW_ICON_PATH),
        size=(25, 25),
    )
    BGCOLOR: str = color("nord13")
    TEXTCOLOR: str = color("nord2")

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes the UpdateButton class with specific styles and properties.

        Args:
            master (ctk.CTkFrame): The parent frame.
        """
        # Initializing the super class
        super().__init__(
            master,
            text="Update Password",
            image=self.ARROW_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, "normal"),
            anchor="center",
            text_color=self.TEXTCOLOR,
            command=self.open_top_level,
        )

        # Storing toplevel window state
        self.toplevel_window = None

    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:
        """
        Custom method to place the button in the grid layout.

        Args:
            row (int): The row position in the grid.
            column (int): The column position in the grid.
            sticky (str): The sticky option for the grid.
        """
        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(5, 10), pady=(10, 5))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:
        """
        Opens the corresponding top-level window for updating a password.
        """
        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = (
                UpdateTopLevel()
            )  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


# Craeting the deletebutton component
class DeleteButton(ctk.CTkButton):
    """
    A custom button class for deleting a password. It initializes with a bin icon and specific styles.

    Attributes:
        BIN_ICON_PATH (str): Path to the bin icon image.
        BIN_IMG (ctk.CTkImage): CustomTkinter image object for the bin icon.
        BGCOLOR (str): Background color for the button.
        TEXTCOLOR (str): Text color for the button.
    """

    # Storing constants to use in class
    BIN_ICON_PATH: str = os.path.join("assets", "icon", "bin.png")
    BIN_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(BIN_ICON_PATH),
        dark_image=Image.open(BIN_ICON_PATH),
        size=(25, 25),
    )
    BGCOLOR: str = color("nord11")
    TEXTCOLOR: str = color("nord2")

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes the DeleteButton class with specific styles and properties.

        Args:
            master (ctk.CTkFrame): The parent frame.
        """
        # Initializing the super class
        super().__init__(
            master,
            text="Delete Password",
            image=self.BIN_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, "normal"),
            anchor="center",
            text_color=self.TEXTCOLOR,
            command=self.open_top_level,
        )

        # Storing toplevel window state
        self.toplevel_window = None

    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:
        """
        Custom method to place the button in the grid layout.

        Args:
            row (int): The row position in the grid.
            column (int): The column position in the grid.
            sticky (str): The sticky option for the grid.
        """
        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(10, 5), pady=5)

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:
        """
        Opens the corresponding top-level window for deleting a password.
        """
        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = (
                DeleteTopLevel()
            )  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


# Craeting the searchbyurlbutton component
class SearchByUrlServiceButton(ctk.CTkButton):
    """
    A custom button class for searching a password by URL or service. It initializes with a URL icon and specific styles.

    Attributes:
        URL_ICON_PATH (str): Path to the URL icon image.
        URL_IMG (ctk.CTkImage): CustomTkinter image object for the URL icon.
        BGCOLOR (str): Background color for the button.
        TEXTCOLOR (str): Text color for the button.
    """

    # Storing constants to use in class
    URL_ICON_PATH: str = os.path.join("assets", "icon", "url.png")
    URL_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(URL_ICON_PATH),
        dark_image=Image.open(URL_ICON_PATH),
        size=(25, 25),
    )
    BGCOLOR: str = color("nord8")
    TEXTCOLOR: str = color("nord2")

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes the SearchByUrlServiceButton class with specific styles and properties.

        Args:
            master (ctk.CTkFrame): The parent frame.
        """
        # Initializing the super class
        super().__init__(
            master,
            text="by Url / Service",
            image=self.URL_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, "normal"),
            anchor="center",
            text_color=self.TEXTCOLOR,
            command=self.open_top_level,
        )

        # Storing toplevel window state
        self.toplevel_window = None

    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:
        """
        Custom method to place the button in the grid layout.

        Args:
            row (int): The row position in the grid.
            column (int): The column position in the grid.
            sticky (str): The sticky option for the grid.
        """
        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(5, 10), pady=5)

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:
        """
        Opens the corresponding top-level window for searching a password by URL or service.
        """
        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SearchTopLevel(
                ("url", "service")
            )  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


# Craeting the searchbyemailorusername component
class SearchByEmailUsernameButton(ctk.CTkButton):
    """
    A custom button class for searching a password by email or username. It initializes with an email icon and specific styles.

    Attributes:
        EMAIL_ICON_PATH (str): Path to the email icon image.
        EMAIL_IMG (ctk.CTkImage): CustomTkinter image object for the email icon.
        BGCOLOR (str): Background color for the button.
        TEXTCOLOR (str): Text color for the button.
    """

    # Storing constants to use in class
    EMAIL_ICON_PATH: str = os.path.join("assets", "icon", "user.png")
    EMAIL_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(EMAIL_ICON_PATH),
        dark_image=Image.open(EMAIL_ICON_PATH),
        size=(25, 25),
    )
    BGCOLOR: str = color("nord4")
    TEXTCOLOR: str = color("nord2")

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes the SearchByEmailUsernameButton class with specific styles and properties.

        Args:
            master (ctk.CTkFrame): The parent frame.
        """
        # Initializing the super class
        super().__init__(
            master,
            text="by Email / User",
            image=self.EMAIL_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, "normal"),
            anchor="center",
            text_color=self.TEXTCOLOR,
            command=self.open_top_level,
        )

        # Storing toplevel window state
        self.toplevel_window = None

    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:
        """
        Custom method to place the button in the grid layout.

        Args:
            row (int): The row position in the grid.
            column (int): The column position in the grid.
            sticky (str): The sticky option for the grid.
        """
        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(10, 5), pady=(5, 10))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:
        """
        Opens the corresponding top-level window for searching a password by email or username.
        """
        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SearchTopLevel(
                ("email", "username")
            )  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


# Craeting the listpassword component
class ListPasswordButton(ctk.CTkButton):
    """
    A custom button class for listing all passwords. It initializes with a list icon and specific styles.

    Attributes:
        LIST_ICON_PATH (str): Path to the list icon image.
        LIST_IMG (ctk.CTkImage): CustomTkinter image object for the list icon.
        BGCOLOR (str): Background color for the button.
        TEXTCOLOR (str): Text color for the button.
    """

    # Storing constants to use in class
    LIST_ICON_PATH: str = os.path.join("assets", "icon", "list.png")
    LIST_IMG: ctk.CTkImage = ctk.CTkImage(
        light_image=Image.open(LIST_ICON_PATH),
        dark_image=Image.open(LIST_ICON_PATH),
        size=(25, 25),
    )
    BGCOLOR: str = color("nord15")
    TEXTCOLOR: str = color("nord2")

    def __init__(self, master: ctk.CTkFrame) -> None:
        """
        Initializes the ListPasswordButton class with specific styles and properties.

        Args:
            master (ctk.CTkFrame): The parent frame.
        """
        # Initializing the super class
        super().__init__(
            master,
            text="List Passwords",
            image=self.LIST_IMG,
            compound=ctk.LEFT,
            fg_color=self.BGCOLOR,
            hover_color=darken_color(self.BGCOLOR),
            font=CustomFont(18, "normal"),
            anchor="center",
            text_color=self.TEXTCOLOR,
            command=self.open_top_level,
        )

        # Storing toplevel window state
        self.toplevel_window = None

    # Function customly grid the button
    def customgrid(self, row: int, column: int, sticky: str) -> None:
        """
        Custom method to place the button in the grid layout.

        Args:
            row (int): The row position in the grid.
            column (int): The column position in the grid.
            sticky (str): The sticky option for the grid.
        """
        # Placing the button
        self.grid(row=row, column=column, sticky=sticky, padx=(5, 10), pady=(5, 10))

    # Function the corresponding toplevel window
    def open_top_level(self) -> None:
        """
        Opens the corresponding top-level window for listing all passwords.
        """
        # Chaking if the toplevel is already opened
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = (
                ListAllTopLevel()
            )  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
