# Importing Libraries
import customtkinter as ctk
from colors.colors import color, darken_color
from components.cancelbutton import CancellButton
from components.customentry import CustomEntry
from components.passwordentry import PasswordEntry
from components.searchform import SearchForm
from database.database import create_password, update_password, delete_password, list_passwords

# Creating the toplevel blueprint for password creation
class CreateTopLevel(ctk.CTkToplevel):

    # Storing constants to use in class
    WINDOW_COLOR: str = color('nord0')
    FRAME_COLOR: str = color('nord1')
    BUTTON_BGCOLOR: str = color('nord14')
    BUTTON_BGCOLOR_DISABLED: str = color('nord0')
    TEXT_COLOR: str = color('nord2')

    def __init__(self) -> None:

        # Initializing the super class
        super().__init__(fg_color=self.WINDOW_COLOR)
        self.resizable(False, False)

        # Configuring the window
        self.size: tuple[int] = (300, 350)
        self.geometry(f'{self.size[0]}x{self.size[1]}')
        self.title('Create Password')

        # Creating the frame
        self.frame: ctk.CTkFrame = ctk.CTkFrame(self,
                                                self.size[0],
                                                self.size[1],
                                                fg_color=self.FRAME_COLOR)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Creating the entries
        self.master_entry: PasswordEntry = PasswordEntry(
            self.frame, 'Master Password')
        self.password_entry: PasswordEntry = PasswordEntry(
            self.frame, 'Password')
        self.email_entry: CustomEntry = CustomEntry(self.frame, 'Email')
        self.username_entry: CustomEntry = CustomEntry(self.frame, 'Username')
        self.url_entry: CustomEntry = CustomEntry(self.frame, 'URL')
        self.service_entry: CustomEntry = CustomEntry(self.frame, 'Service')

        # Placing the entries
        self.master_entry.pack(
            pady=(
                10,
                5),
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.password_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.email_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.username_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.url_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.service_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)

        # Bind the function to entry changes
        self.master_entry.entry.bind(
            '<KeyRelease>',
            lambda _: self.update_create_button_state())
        self.password_entry.bind('<KeyRelease>',
                                 lambda _: self.update_create_button_state())
        self.email_entry.bind('<KeyRelease>',
                              lambda _: self.update_create_button_state())
        self.username_entry.bind('<KeyRelease>',
                                 lambda _: self.update_create_button_state())
        self.url_entry.bind('<KeyRelease>',
                            lambda _: self.update_create_button_state())
        self.service_entry.bind('<KeyRelease>',
                                lambda _: self.update_create_button_state())

        # Creating the 2 buttons, enter and cancel
        self.create_btn: ctk.CTkButton = ctk.CTkButton(
            self.frame,
            text='Create',
            fg_color=self.BUTTON_BGCOLOR,
            text_color=self.TEXT_COLOR,
            hover_color=darken_color(self.BUTTON_BGCOLOR),
            command=self.create_password)
        self.create_btn.pack(side=ctk.LEFT, padx=10, pady=10)

        # Set the initial state of the create button
        self.update_create_button_state()

        self.cancel_btn: CancellButton = CancellButton(self.frame, self)
        self.cancel_btn.pack(side=ctk.LEFT, padx=10, pady=10)

    # Method to get the values from the entries
    def get_entry_values(self) -> tuple[str]:
        return (
            entry.get() for entry in [
                self.master_entry.entry,
                self.password_entry.entry,
                self.email_entry,
                self.username_entry,
                self.url_entry,
                self.service_entry])

    # Method to update the state of the create button
    def update_create_button_state(self) -> None:

        # Getting all the values
        values = list(self.get_entry_values())

        # Check the condition,  perform state change based on it
        if all(values[:2]) and any(values[2:]):
            self.create_btn.configure(
                state='normal', fg_color=self.BUTTON_BGCOLOR)
        else:
            self.create_btn.configure(
                state='disabled',
                fg_color=self.BUTTON_BGCOLOR_DISABLED)

    # Method for creating a new password based on the inputed entries
    def create_password(self) -> None:

        # Committing the password
        create_password(*self.get_entry_values())

        # Destroing the toplevel
        self.destroy()

# Creating the toplevel blueprint for password updates
class UpdateTopLevel(ctk.CTkToplevel):

    # Storing constants to use in class
    WINDOW_COLOR: str = color('nord0')
    FRAME_COLOR: str = color('nord1')
    BUTTON_BGCOLOR: str = color('nord13')
    BUTTON_BGCOLOR_DISABLED: str = color('nord0')
    TEXT_COLOR: str = color('nord2')

    def __init__(self) -> None:

        # Initializing the super class
        super().__init__(fg_color=self.WINDOW_COLOR)
        self.resizable(False, False)

        # Configuring the window
        self.size: tuple[int] = (300, 350)
        self.geometry(f'{self.size[0]}x{self.size[1]}')
        self.title('Update Password')

        # Creating the frame
        self.frame: ctk.CTkFrame = ctk.CTkFrame(self,
                                                self.size[0],
                                                self.size[1],
                                                fg_color=self.FRAME_COLOR)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Creating the entries
        self.master_entry: PasswordEntry = PasswordEntry(
            self.frame, 'Master Password')
        self.new_password_entry: PasswordEntry = PasswordEntry(
            self.frame, 'New Password')
        self.email_entry: CustomEntry = CustomEntry(self.frame, 'Email')
        self.username_entry: CustomEntry = CustomEntry(self.frame, 'Username')
        self.url_entry: CustomEntry = CustomEntry(self.frame, 'URL')
        self.service_entry: CustomEntry = CustomEntry(self.frame, 'Service')

        # Placing the entries
        self.master_entry.pack(
            pady=(
                10,
                5),
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.new_password_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.email_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.username_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.url_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.service_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)

        # Bind the function to entry changes
        self.master_entry.entry.bind(
            '<KeyRelease>',
            lambda _: self.update_update_button_state())
        self.new_password_entry.bind(
            '<KeyRelease>',
            lambda _: self.update_update_button_state())
        self.email_entry.bind('<KeyRelease>',
                              lambda _: self.update_update_button_state())
        self.username_entry.bind('<KeyRelease>',
                                 lambda _: self.update_update_button_state())
        self.url_entry.bind('<KeyRelease>',
                            lambda _: self.update_update_button_state())
        self.service_entry.bind('<KeyRelease>',
                                lambda _: self.update_update_button_state())

        # Creating the 2 buttons, enter and cancel
        self.update_btn: ctk.CTkButton = ctk.CTkButton(
            self.frame,
            text='Update',
            fg_color=self.BUTTON_BGCOLOR,
            text_color=self.TEXT_COLOR,
            hover_color=darken_color(self.BUTTON_BGCOLOR),
            command=self.update_password)
        self.update_btn.pack(side=ctk.LEFT, padx=10, pady=10)

        # Set the initial state of the update button
        self.update_update_button_state()

        self.cancel_btn: CancellButton = CancellButton(self.frame, self)
        self.cancel_btn.pack(side=ctk.LEFT, padx=10, pady=10)

    # Method to get the values from the entries
    def get_entry_values(self) -> tuple[str]:
        return (
            entry.get() for entry in [
                self.master_entry.entry,
                self.new_password_entry.entry,
                self.email_entry,
                self.username_entry,
                self.url_entry,
                self.service_entry])

    # Method to update the state of the create button
    def update_update_button_state(self) -> None:

        # Getting all the values
        values = list(self.get_entry_values())

        # Check the condition,  perform state change based on it
        if all(values[:2]) and any(values[2:]):
            self.update_btn.configure(
                state='normal', fg_color=self.BUTTON_BGCOLOR)
        else:
            self.update_btn.configure(
                state='disabled',
                fg_color=self.BUTTON_BGCOLOR_DISABLED)

    # Method for updating an existing password based on the inputed entries
    def update_password(self) -> None:

        # Committing the password
        update_password(*self.get_entry_values())

        # Destroing the toplevel
        self.destroy()

# Creating the toplevel blueprint for password deletition
class DeleteTopLevel(ctk.CTkToplevel):

    # Storing constants to use in class
    WINDOW_COLOR: str = color('nord0')
    FRAME_COLOR: str = color('nord1')
    BUTTON_BGCOLOR: str = color('nord11')
    BUTTON_BGCOLOR_DISABLED: str = color('nord0')
    TEXT_COLOR: str = color('nord4')

    def __init__(self) -> None:

        # Initializing the super class
        super().__init__(fg_color=self.WINDOW_COLOR)
        self.resizable(False, False)

        # Configuring the window
        self.size: tuple[int] = (300, 350)
        self.geometry(f'{self.size[0]}x{self.size[1]}')
        self.title('Delete Password')

        # Creating the frame
        self.frame: ctk.CTkFrame = ctk.CTkFrame(self,
                                                self.size[0],
                                                self.size[1],
                                                fg_color=self.FRAME_COLOR)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Creating the entries
        self.email_entry: CustomEntry = CustomEntry(self.frame, 'Email')
        self.username_entry: CustomEntry = CustomEntry(self.frame, 'Username')
        self.url_entry: CustomEntry = CustomEntry(self.frame, 'URL')
        self.service_entry: CustomEntry = CustomEntry(self.frame, 'Service')

        # Placing the entries
        self.email_entry.pack(
            pady=(
                10,
                5),
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.username_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.url_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)
        self.service_entry.pack(
            pady=5,
            padx=10,
            anchor='w',
            expand=True,
            fill=ctk.BOTH)

        # Bind the function to entry changes
        self.email_entry.bind('<KeyRelease>',
                              lambda _: self.update_delete_button_state())
        self.username_entry.bind('<KeyRelease>',
                                 lambda _: self.update_delete_button_state())
        self.url_entry.bind('<KeyRelease>',
                            lambda _: self.update_delete_button_state())
        self.service_entry.bind('<KeyRelease>',
                                lambda _: self.update_delete_button_state())

        # Creating the 2 buttons, enter and cancel
        self.delete_btn: ctk.CTkButton = ctk.CTkButton(
            self.frame,
            text='Delete',
            fg_color=self.BUTTON_BGCOLOR,
            text_color=self.TEXT_COLOR,
            hover_color=darken_color(self.BUTTON_BGCOLOR),
            command=self.delete_password)
        self.delete_btn.pack(side=ctk.LEFT, padx=10, pady=10)

        # Set the initial state of the delete button
        self.update_delete_button_state()

        self.cancel_btn: CancellButton = CancellButton(self.frame, self)
        self.cancel_btn.pack(side=ctk.LEFT, padx=10, pady=10)

    # Method to get the values from the entries
    def get_entry_values(self) -> tuple[str]:
        return (
            entry.get() for entry in [
                self.email_entry,
                self.username_entry,
                self.url_entry,
                self.service_entry])

    # Method to update the state of the create button
    def update_delete_button_state(self) -> None:

        # Getting all the values
        values = list(self.get_entry_values())

        # Check the condition,  perform state change based on it
        if any(values):
            self.delete_btn.configure(
                state='normal', fg_color=self.BUTTON_BGCOLOR)
        else:
            self.delete_btn.configure(
                state='disabled',
                fg_color=self.BUTTON_BGCOLOR_DISABLED)

    # Method for deleting an existing password based on the inputed entries
    def delete_password(self) -> None:

        # Committing the password
        delete_password(*self.get_entry_values())

        # Destroing the toplevel
        self.destroy()

# Creating the toplevel blueprint for searching password by url / service
class SearchTopLevel(ctk.CTkToplevel):

    # Storing constants to use in class
    WINDOW_COLOR: str = color('nord0')
    FRAME_COLOR: str = color('nord1')
    BUTTON_BGCOLOR: str = color('nord2')
    BUTTON_SELECTED_COLOR: str = color('nord10')
    SEARCH_BGCOLOR: str = color('nord7')
    DISABLED_SEARCH_BGCOLOR: str = color('nord0')
    TEXT_COLOR: str = color('nord2')
    SCROLLBAR_COLOR: str = color('nord3')

    def __init__(self, filter_couple: tuple[str, str]) -> None:

        # Initializing the super class
        super().__init__(fg_color=self.WINDOW_COLOR)
        self.resizable(False, False)

        # Configuring the window
        self.size: tuple[int] = (300, 475)
        self.geometry(f'{self.size[0]}x{self.size[1]}')
        self.title('Search Password')

        # Creating the tabview for choosing the searching method
        tabview: ctk.CTkTabview = ctk.CTkTabview(
            self,
            fg_color=self.FRAME_COLOR,
            segmented_button_fg_color=self.BUTTON_BGCOLOR,
            segmented_button_selected_color=self.BUTTON_SELECTED_COLOR,
            segmented_button_selected_hover_color=darken_color(
                self.BUTTON_SELECTED_COLOR),
            segmented_button_unselected_color=self.BUTTON_BGCOLOR,
            segmented_button_unselected_hover_color=darken_color(
                self.BUTTON_BGCOLOR))
        
        # Adding and placing the tabs
        url_tab: ctk.CTkFrame = tabview.add(filter_couple[0].capitalize())
        service_tab: ctk.CTkFrame = tabview.add(filter_couple[1].capitalize())
        tabview.pack(padx=10, pady=(0, 10), fill=ctk.BOTH, expand=True)

        # Fill the two tabs with the corresponding widgets
        SearchForm(url_tab, filter_couple[0], self)
        SearchForm(service_tab, filter_couple[1], self)

# Creating the blueprint to list all passwords
class ListAllTopLevel(ctk.CTkToplevel):

    # Storing constants to use in class
    WINDOW_COLOR: str = color('nord0')
    FRAME_COLOR: str = color('nord1')
    LIST_BGCOLOR: str = color('nord15')
    DISABLED_LIST_BGCOLOR: str = color('nord0')
    TEXT_COLOR: str = color('nord2')
    SCROLLBAR_COLOR: str = color('nord3')

    def __init__(self) -> None:

        # Initializing the super class
        super().__init__(fg_color=self.WINDOW_COLOR)
        self.resizable(False, False)

        # Configuring the window
        self.size: tuple[int] = (300, 400)
        self.geometry(f'{self.size[0]}x{self.size[1]}')
        self.title('List Passwords')

        # Creating the frame
        self.frame: ctk.CTkFrame = ctk.CTkFrame(self,
                                                self.size[0],
                                                self.size[1],
                                                fg_color=self.FRAME_COLOR)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Creating and placing the widgets
        self.master_entry: PasswordEntry = PasswordEntry(self.frame, 'Master Password')
        self.srcollable_frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(self.frame,
                                                                               width=300,
                                                                               height=50,
                                                                               label_text='Passwords', 
                                                                               label_fg_color=color('nord3'),
                                                                               fg_color=color('nord2'),
                                                                               scrollbar_button_color=self.SCROLLBAR_COLOR,
                                                                               scrollbar_button_hover_color=darken_color(self.SCROLLBAR_COLOR))
        self.master_entry.pack(padx=10, pady=(10, 5), anchor='w', expand=True, fill=ctk.BOTH)
        self.srcollable_frame.pack(padx=10, pady=(5, 10), anchor='w', expand=True, fill=ctk.BOTH)
        self.password_label_text: ctk.StringVar = ctk.StringVar()
        self.password_label_text.set('')
        self.password_label: ctk.CTkLabel = ctk.CTkLabel(self.srcollable_frame, textvariable=self.password_label_text, font=('Arial', 18))
        self.password_label.pack()

        # Bind the function to entry changes
        self.master_entry.bind('<KeyRelease>',
                               lambda _: self.update_search_button_state())
        
        # Creating the 2 buttons, enter and cancel
        self.search_btn: ctk.CTkButton = ctk.CTkButton(
            self.frame,
            text='List',
            fg_color=self.LIST_BGCOLOR,
            text_color=self.TEXT_COLOR,
            hover_color=darken_color(self.LIST_BGCOLOR),
            command=self.list_password)
        self.search_btn.pack(side=ctk.LEFT, padx=10, pady=10)

        # Set the initial state of the delete button
        self.update_list_button_state()

        self.cancel_btn: CancellButton = CancellButton(self.frame, self)
        self.cancel_btn.pack(side=ctk.LEFT, padx=10, pady=10)
    
    # Method to get the values from the entries
    def get_entry_values(self) -> str:
        return self.master_entry.entry.get()
    
    # Method to update the state of the create button
    def update_list_button_state(self) -> None:

        # Getting all the values
        values = list(self.get_entry_values())

        # Check the condition,  perform state change based on it
        if all(values):
            self.search_btn.configure(
                state='normal', fg_color=self.LIST_BGCOLOR)
        else:
            self.search_btn.configure(
                state='disabled',
                fg_color=self.DISABLED_LIST_BGCOLOR)

    # Method for showing passwords in the frame based on the parameters
    def list_password(self) -> None:

        # Fetching all the passwords corresponding to a certain criteria value
        passwords_list: list = list_passwords(self.get_entry_values())

        # Creating password text to display on the scrollable frame
        passwords_text: str = '\n'.join(passwords_list)

        # Modifing the scrollable frame label
        self.password_label_text.set(passwords_text)
