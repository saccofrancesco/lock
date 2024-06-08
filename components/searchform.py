# Importing Libraries
import customtkinter as ctk
from colors.colors import color, darken_color
from components.cancelbutton import CancellButton
from components.customentry import CustomEntry
from components.passwordentry import PasswordEntry
from database.database import search_password

# Creating the blueprint for the form to search passwords by a given criteria
class SearchForm():
    """
    A custom form class for searching passwords based on given criteria.

    Attributes:
        BUTTON_BGCOLOR (str): Background color for the buttons.
        SCROLLBAR_COLOR (str): Color for the scrollbar.
        SEARCH_BGCOLOR (str): Background color for the search button.
        TEXT_COLOR (str): Text color for the buttons.
        DISABLED_SEARCH_BGCOLOR (str): Background color for the disabled search button.
    """
    # Storing constants to use in class
    BUTTON_BGCOLOR: str = color('nord2')
    SCROLLBAR_COLOR: str = color('nord3')
    SEARCH_BGCOLOR: str = color('nord7')
    TEXT_COLOR: str = color('nord2')
    DISABLED_SEARCH_BGCOLOR: str = color('nord0')

    def __init__(self, master: ctk.CTkFrame, criteria: str, top: ctk.CTkToplevel) -> None:
        """
        Initializes the SearchForm class with specified master widget, search criteria, and top-level window.

        Args:
            master (ctk.CTkFrame): The parent widget.
            criteria (str): The criteria to search passwords by.
            top (ctk.CTkToplevel): The top-level window to be closed by the cancel button.
        """
        # Saving form criteria
        self.criteria: str = criteria

        # Fill the two tabs with the corresponding widgets
        self.master_entry: PasswordEntry = PasswordEntry(master, 'Master Password')
        self.criteria_entry: CustomEntry = CustomEntry(master, f'Enter {criteria.capitalize()} to search')
        self.srcollable_frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(master,
                                                                               width=300,
                                                                               height=50,
                                                                               label_text='Passwords', 
                                                                               label_fg_color=color('nord3'),
                                                                               fg_color=self.BUTTON_BGCOLOR,
                                                                               scrollbar_button_color=self.SCROLLBAR_COLOR,
                                                                               scrollbar_button_hover_color=darken_color(self.SCROLLBAR_COLOR))
        self.master_entry.pack(padx=10, pady=5, anchor='w', expand=True, fill=ctk.BOTH)
        self.criteria_entry.pack(padx=10, pady=5, anchor='w', expand=True, fill=ctk.BOTH)
        self.srcollable_frame.pack(padx=10, pady=(5, 10), anchor='w', expand=True, fill=ctk.BOTH)
        self.password_label_text: ctk.StringVar = ctk.StringVar()
        self.password_label_text.set('')
        self.password_label: ctk.CTkLabel = ctk.CTkLabel(self.srcollable_frame, textvariable=self.password_label_text, font=('Arial', 18))
        self.password_label.pack()

        # Bind the function to entry changes
        self.master_entry.bind('<KeyRelease>',
                               lambda _: self.update_search_button_state())
        self.criteria_entry.bind('<KeyRelease>',
                               lambda _: self.update_search_button_state())
        
        # Creating the 2 buttons, enter and cancel
        self.search_btn: ctk.CTkButton = ctk.CTkButton(
            master,
            text='Search',
            fg_color=self.SEARCH_BGCOLOR,
            text_color=self.TEXT_COLOR,
            hover_color=darken_color(self.SEARCH_BGCOLOR),
            command=self.search_password)
        self.search_btn.pack(side=ctk.LEFT, padx=10, pady=10)

        # Set the initial state of the delete button
        self.update_search_button_state()

        self.cancel_btn: CancellButton = CancellButton(master, top)
        self.cancel_btn.pack(side=ctk.LEFT, padx=10, pady=10)

    # Method to get the values from the entries
    def get_entry_values(self) -> tuple[str]:
        """
        Retrieves the values from the entry fields.

        Returns:
            tuple[str, str]: The values entered in the master password and criteria entry fields.
        """
        return (
            entry.get() for entry in [
                self.master_entry.entry,
                self.criteria_entry])
    
    # Method to update the state of the create button
    def update_search_button_state(self) -> None:
        """
        Updates the state of the search button based on the presence of text in the entry fields.
        """
        # Getting all the values
        values = list(self.get_entry_values())

        # Check the condition,  perform state change based on it
        if all(values):
            self.search_btn.configure(
                state='normal', fg_color=self.SEARCH_BGCOLOR)
        else:
            self.search_btn.configure(
                state='disabled',
                fg_color=self.DISABLED_SEARCH_BGCOLOR)
    
    # Method for showing passwords in the frame based on the parameters
    def search_password(self) -> None:
        """
        Searches for passwords based on the criteria and updates the scrollable frame with the results.
        """
        # Fetching all the passwords corresponding to a certain criteria value
        passwords_list: list = search_password(self.master_entry.entry.get(), self.criteria, self.criteria_entry.get())

        # Creating password text to display on the scrollable frame
        passwords_text: str = '\n'.join(passwords_list)

        # Modifing the scrollable frame label
        self.password_label_text.set(passwords_text)
