# module/dialogs.py

from tkinter import filedialog, colorchooser, messagebox

def open_file_dialog(self, filetypes=(("All files", "*.*"),)):
    """
    Open a file dialog to allow the user to select a file.
    
    :param filetypes: A tuple specifying the types of files that can be selected.
    :return: The path of the selected file (string).
    """
    return filedialog.askopenfilename(filetypes=filetypes)

def open_color_dialog(self):
    """
    Open a color chooser dialog to allow the user to select a color.
    
    :return: The selected color in hexadecimal format (e.g., "#FFFFFF").
    """
    color = colorchooser.askcolor()[1]
    return color

def show_messagebox(self, title, message):
    """
    Show an information messagebox.
    
    :param title: The title of the messagebox.
    :param message: The message text to display in the messagebox.
    """
    messagebox.showinfo(title, message)

def show_error_messagebox(self, title, message):
    """
    Show an error messagebox.
    
    :param title: The title of the messagebox.
    :param message: The error message text to display in the messagebox.
    """
    messagebox.showerror(title, message)

def show_warning_messagebox(self, title, message):
    """
    Show a warning messagebox.
    
    :param title: The title of the messagebox.
    :param message: The warning message text to display in the messagebox.
    """
    messagebox.showwarning(title, message)

def ask_yes_no(self, title, message):
    """
    Show a confirmation dialog to allow the user to choose "Yes" or "No".
    
    :param title: The title of the confirmation dialog.
    :param message: The message text to display in the dialog.
    :return: The user's choice as a boolean value (True for "Yes", False for "No").
    """
    return messagebox.askyesno(title, message)
