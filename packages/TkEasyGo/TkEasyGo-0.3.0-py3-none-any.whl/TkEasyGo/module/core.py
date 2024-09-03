# module/core.py

import tkinter as tk
import ttkbootstrap as tb

class SimpleWindow:
    """A simple GUI window using Tkinter and ttkbootstrap with various helper methods."""

    def __init__(self, title="TkEasyGo Window", width=300, height=200):
        """
        Initialize the window with a title, width, and height.
        
        :param title: The title of the window.
        :param width: The initial width of the window.
        :param height: The initial height of the window.
        """
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.style = tb.Style()  # Use ttkbootstrap's style
        self.configure_styles()
        self.widgets = {}
        self.current_row = 0
        self.current_column = 0
        self.frames = {}
        self.maximized = False
        self.grid_config = {'padx': 10, 'pady': 10, 'sticky': "ew"}  # Default grid configuration

    def configure_styles(self):
        """
        Configure the styles for various ttkbootstrap widgets.
        """
        self.style.configure('TButton', padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
        self.style.configure('TLabel', background="#f4f4f4", font=("Arial", 12))
        self.style.configure('TEntry', padding=5, relief="flat", font=("Arial", 12))
        self.style.configure('TCheckbutton', background="#f4f4f4", font=("Arial", 12))
        self.style.configure('TRadiobutton', background="#f4f4f4", font=("Arial", 12))
        self.style.configure('TCombobox', padding=5, relief="flat", font=("Arial", 12))
        self.style.configure('TProgressbar', thickness=10, troughcolor='#d0d0d0', background='#4CAF50')
        self.style.configure('TSpinbox', padding=5, relief="flat", font=("Arial", 12))
        self.style.configure('TNotebook', tabposition='n', background='#f4f4f4')
        self.style.configure('TLabelFrame', background='#f4f4f4', font=("Arial", 12))
        self.style.configure('TSeparator', background='#d0d0d0')
        self.style.configure('TPanedwindow', background='#f4f4f4')

    def update_style(self, style_name, options):
        """
        Update the style configuration for a given widget style.
        
        :param style_name: The name of the style to be updated.
        :param options: A dictionary of style options to apply.
        """
        self.style.configure(style_name, **options)

    def set_grid_config(self, **options):
        """
        Set the default grid configuration for all widgets.
        
        :param options: Grid configuration options (e.g., padx, pady, sticky).
        """
        self.grid_config.update(options)

    def run(self):
        """
        Run the Tkinter main loop.
        """
        self.root.mainloop()

    def maximize(self):
        """
        Maximize the window to fullscreen.
        """
        self.root.attributes("-fullscreen", True)
        self.maximized = True

    def minimize(self):
        """
        Minimize the window to the taskbar.
        """
        self.root.iconify()

    def restore(self):
        """
        Restore the window to its normal size.
        """
        self.root.attributes("-fullscreen", False)
        self.maximized = False

    def log(self, message):
        """
        Log a message. Currently, it prints to the console.
        
        :param message: The message to log.
        """
        print(f"[LOG]: {message}")

    def add_frame(self, frame_name, row=None, column=None, rowspan=1, columnspan=1):
        """
        Add a frame to the main window and keep track of it.
        
        :param frame_name: The name to associate with the frame.
        :param row: The row position for grid layout.
        :param column: The column position for grid layout.
        :param rowspan: The number of rows the frame should span.
        :param columnspan: The number of columns the frame should span.
        :return: The created frame.
        """
        frame = tk.Frame(self.root)
        frame.grid(row=row if row is not None else self.current_row,
                   column=column if column is not None else self.current_column,
                   rowspan=rowspan,
                   columnspan=columnspan,
                   **self.grid_config)
        self.frames[frame_name] = frame
        return frame

    def add_widget(self, widget_name, widget, row=None, column=None, rowspan=1, columnspan=1):
        """
        Add a widget to the window and keep track of it.
        
        :param widget_name: The name to associate with the widget.
        :param widget: The widget to add.
        :param row: The row position for grid layout.
        :param column: The column position for grid layout.
        :param rowspan: The number of rows the widget should span.
        :param columnspan: The number of columns the widget should span.
        :return: The added widget.
        """
        widget.grid(row=row if row is not None else self.current_row,
                    column=column if column is not None else self.current_column,
                    rowspan=rowspan,
                    columnspan=columnspan,
                    **self.grid_config)
        self.widgets[widget_name] = widget
        if row is None:
            self.current_row += 1
        if column is None:
            self.current_column += 1
        return widget
