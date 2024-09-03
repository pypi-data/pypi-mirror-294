from .module.core import SimpleWindow as BaseSimpleWindow
from .module.widgets import *
from .module.dialogs import *
from .module.utils import *
class SimpleWindow(BaseSimpleWindow):
    """Main SimpleWindow class that integrates core, widgets, dialogs, and utils."""

    def __init__(self, title="TkEasyGo Window", width=300, height=200):
        super().__init__(title, width, height)

    # Widget methods
    add_button = add_button
    add_label = add_label
    add_textbox = add_textbox
    add_checkbox = add_checkbox
    add_radiobutton = add_radiobutton
    add_combobox = add_combobox
    add_progressbar = add_progressbar
    add_slider = add_slider
    add_notebook = add_notebook
    add_label_frame = add_label_frame
    add_spinbox = add_spinbox
    add_canvas = add_canvas
    add_calendar = add_calendar
    add_treeview = add_treeview
    add_tooltip = add_tooltip
    add_context_menu = add_context_menu
    add_text = add_text
    add_listbox = add_listbox
    add_scrollbar = add_scrollbar
    add_message = add_message
    add_paned_window = add_paned_window
    add_separator = add_separator
    _add_widget = add_widget
    add_menu=add_menu
    add_menubutton=add_menubutton
    add_text=add_text
    add_option_menu=add_option_menu
    add_image=add_image
    add_file_dialog=add_file_dialog
    

    # Dialog methods
    open_file_dialog = open_file_dialog
    open_color_dialog = open_color_dialog
    show_messagebox = show_messagebox
    show_error_messagebox = show_error_messagebox
    show_warning_messagebox = show_warning_messagebox
    ask_yes_no = ask_yes_no

    # Utility methods
    bind_event = bind_event
    bind_events = bind_events
    disable_widget = disable_widget
    enable_widget = enable_widget
    remove_widget = remove_widget

    def __getattr__(self, name):
        """
        Handle calls to methods that are not directly defined in this class.
        
        :param name: The name of the method or attribute.
        :return: The corresponding method from the base class or the imported methods.
        """
        if name in dir(self):
            return getattr(self, name)
        elif name in globals():
            return globals()[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    # Optionally add more methods or properties if needed
