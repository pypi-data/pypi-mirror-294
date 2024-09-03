#module/widgets.py

import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import Calendar  # Ensure you have installed tkcalendar using 'pip install tkcalendar'

def add_button(self, text, command, row=None, column=None, rowspan=1, columnspan=1, style=None, width=None, height=None, frame=None):
    """
    Add a button to the window.

    :param text: The text on the button.
    :param command: The callback function when the button is clicked.
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :param style: Button style.
    :param width: Width of the button.
    :param height: Height of the button.
    :param frame: The frame to add the button to, defaults to the root frame.
    :return: The created button widget.
    """
    frame = frame or self.root
    button = ttk.Button(frame, text=text, command=command, style='TButton')
    
    if width:
        button.config(width=width)
    if height:
        button.config(height=height)
    if style:
        button.config(**style)
    
    self.widgets['button'] = self._add_widget(button, row, column, rowspan, columnspan)
    return button


def add_label(self, text, row=None, column=None, rowspan=1, columnspan=1, style=None, font=None, frame=None):
    """
    Add a label to the window.

    :param text: The text on the label.
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :param style: Label style.
    :param font: Font of the label (e.g., ("Helvetica", 12)).
    :param frame: The frame to add the label to, defaults to the root frame.
    :return: The created label widget.
    """
    frame = frame or self.root
    label = ttk.Label(frame, text=text, style='TLabel')
    if font:
        label.config(font=font)
    if style:
        label.config(**style)
    self.widgets['label'] = self._add_widget(label, row, column, rowspan, columnspan)
    return label

def add_textbox(self, default_text="", width=20, row=None, column=None, rowspan=1, columnspan=1, style=None, font=None, height=1, frame=None):
    """
    Add a textbox to the window.

    :param default_text: Default text for the textbox.
    :param width: Width of the textbox.
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :param style: Textbox style.
    :param font: Font of the textbox (e.g., ("Helvetica", 12)).
    :param height: Height of the textbox; if greater than 1, a multi-line textbox is created.
    :param frame: The frame to add the textbox to, defaults to the root frame.
    :return: The created textbox widget.
    """
    frame = frame or self.root
    if height > 1:
        textbox = tk.Text(frame, width=width, height=height)
        textbox.insert(tk.END, default_text)
    else:
        textbox = ttk.Entry(frame, width=width, style='TEntry')
        textbox.insert(0, default_text)
    if font:
        textbox.config(font=font)
    if style:
        textbox.config(**style)
    self.widgets['textbox'] = self._add_widget(textbox, row, column, rowspan, columnspan)
    return textbox

def add_checkbox(self, text, variable, row=None, column=None, rowspan=1, columnspan=1, style=None, onvalue=1, offvalue=0, frame=None):
    """
    Add a checkbox to the window.

    :param text: The text on the checkbox.
    :param variable: Tkinter variable associated with the checkbox.
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :param style: Checkbox style.
    :param onvalue: The value associated with the variable when the checkbox is checked.
    :param offvalue: The value associated with the variable when the checkbox is unchecked.
    :param frame: The frame to add the checkbox to, defaults to the root frame.
    :return: The created checkbox widget.
    """
    frame = frame or self.root
    checkbox = ttk.Checkbutton(frame, text=text, variable=variable.var, onvalue=onvalue, offvalue=offvalue, style='TCheckbutton')
    if style:
        checkbox.config(**style)
    self.widgets['checkbox'] = self._add_widget(checkbox, row, column, rowspan, columnspan)
    return checkbox


def add_radiobutton(self, text, value, variable, row=None, column=None, style=None, frame=None):
    """
    Add a radiobutton to the window.
    
    :param text: The text on the radiobutton.
    :param value: The value of the radiobutton.
    :param variable: Tkinter variable associated with the radiobutton.
    :param row: Row position.
    :param column: Column position.
    :param style: Radiobutton style.
    :param frame: The frame to add the radiobutton to, defaults to the root frame.
    :return: The created radiobutton widget.
    """
    frame = frame or self.root
    radiobutton = ttk.Radiobutton(frame, text=text, value=value, variable=variable.var, style='TRadiobutton')
    if style:
        radiobutton.config(**style)
    self.widgets['radiobutton'] = self._add_widget(radiobutton, row, column)
    return radiobutton


def add_combobox(self, values, row=None, column=None, width=None, style=None, frame=None):
    """
    Add a combobox to the window.
    
    :param values: List of values for the combobox.
    :param row: Row position.
    :param column: Column position.
    :param width: Width of the combobox.
    :param style: Combobox style.
    :param frame: The frame to add the combobox to, defaults to the root frame.
    :return: The created combobox widget.
    """
    frame = frame or self.root
    combobox = ttk.Combobox(frame, values=values, style='TCombobox')
    if width:
        combobox.config(width=width)
    if style:
        combobox.config(**style)
    self.widgets['combobox'] = self._add_widget(combobox, row, column)
    return combobox


def add_progressbar(self, maximum=100, value=0, mode='determinate', row=None, column=None, columnspan=1, style=None, frame=None):
    """
    Add a progressbar to the window.
    
    :param maximum: Maximum value of the progressbar.
    :param value: Current value of the progressbar.
    :param mode: Mode of the progressbar ('determinate' or 'indeterminate').
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param style: Progressbar style.
    :param frame: The frame to add the progressbar to, defaults to the root frame.
    :return: The created progressbar widget.
    """
    frame = frame or self.root
    progressbar = ttk.Progressbar(frame, maximum=maximum, value=value, mode=mode, style='TProgressbar')
    if style:
        progressbar.config(**style)
    self.widgets['progressbar'] = self._add_widget(progressbar, row, column, columnspan=columnspan)
    return progressbar


def add_slider(self, from_=0, to=100, orient=tk.HORIZONTAL, value=0, length=200, sliderlength=30, row=None, column=None, columnspan=1, style=None, frame=None):
    """
    Add a slider to the window.
    
    :param from_: Minimum value of the slider.
    :param to: Maximum value of the slider.
    :param orient: Orientation of the slider (HORIZONTAL or VERTICAL).
    :param value: Current value of the slider.
    :param length: Length of the slider.
    :param sliderlength: Length of the slider button.
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param style: Slider style.
    :param frame: The frame to add the slider to, defaults to the root frame.
    :return: The created slider widget.
    """
    frame = frame or self.root
    slider = tk.Scale(frame, from_=from_, to=to, orient=orient, length=length, sliderlength=sliderlength)
    slider.set(value)
    if style:
        slider.config(**style)
    self.widgets['slider'] = self._add_widget(slider, row, column, columnspan=columnspan)
    return slider


def add_notebook(self, tabs, row=None, column=None, rowspan=1, columnspan=1, style=None, padding=None):
    """
    Add a notebook (tabbed interface) to the window.
    
    :param tabs: Dictionary where keys are tab names and values are functions to create tab content.
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :param style: Notebook style.
    :param padding: Padding inside the notebook.
    :return: The created notebook widget.
    """
    notebook = ttk.Notebook(self.root, style='TNotebook')
    if padding:
        notebook.config(padding=padding)
    if style:
        notebook.config(**style)
    for tab_name, content in tabs.items():
        frame = tk.Frame(notebook)
        content(self, frame)
        notebook.add(frame, text=tab_name)
    self.widgets['notebook'] = self._add_widget(notebook, row, column, rowspan, columnspan)
    return notebook


def add_label_frame(self, text, row=None, column=None, rowspan=1, columnspan=1, style=None, padding=None):
    """
    Add a label frame (grouping widget) to the window.
    
    :param text: The text on the label frame.
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :param style: Label frame style.
    :param padding: Padding inside the label frame.
    :return: The created label frame widget.
    """
    frame = ttk.LabelFrame(self.root, text=text, style='TLabelFrame')
    if style:
        frame.config(**style)
    if padding:
        frame.config(padding=padding)
    self.widgets['label_frame'] = self._add_widget(frame, row, column, rowspan, columnspan)
    return frame

def add_spinbox(self, from_, to, increment=1, row=None, column=None, style=None, frame=None, wrap=False):
    """
    Add a spinbox to the window.
    
    :param from_: Minimum value of the spinbox.
    :param to: Maximum value of the spinbox.
    :param increment: Increment value of the spinbox.
    :param row: Row position.
    :param column: Column position.
    :param style: Spinbox style.
    :param frame: The frame to add the spinbox to, defaults to the root frame.
    :param wrap: Whether to wrap the spinbox values.
    :return: The created spinbox widget.
    """
    frame = frame or self.root
    spinbox = ttk.Spinbox(frame, from_=from_, to=to, increment=increment, wrap=wrap, style='TSpinbox')
    if style:
        spinbox.config(**style)
    self.widgets['spinbox'] = self._add_widget(spinbox, row, column)
    return spinbox

def add_canvas(self, width, height, row=None, column=None, columnspan=1, bg=None):
    """
    Add a canvas to the window.
    
    :param width: Width of the canvas.
    :param height: Height of the canvas.
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param bg: Background color of the canvas.
    :return: The created canvas widget.
    """
    canvas = tk.Canvas(self.root, width=width, height=height, bg=bg)
    self.widgets['canvas'] = self._add_widget(canvas, row, column, columnspan=columnspan)
    return canvas

def add_calendar(self, row=None, column=None, firstweekday='sunday'):
    """
    Add a calendar to the window.
    
    :param row: Row position.
    :param column: Column position.
    :param firstweekday: First day of the week.
    :return: The created calendar widget.
    """
    frame = tk.Frame(self.root)
    frame.grid(row=row if row is not None else self.current_row,
               column=column if column is not None else self.current_column,
               **self.grid_config)
    
    calendar = Calendar(frame, selectmode='day', firstweekday=firstweekday)
    calendar.pack(padx=10, pady=10, expand=True, fill='both')
    
    self.widgets['calendar'] = calendar
    return calendar

def add_treeview(self, columns, row=None, column=None, columnspan=1, style=None, frame=None, show='headings'):
    """
    Add a treeview to the window.
    
    :param columns: List of column names.
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param style: Treeview style.
    :param frame: The frame to add the treeview to, defaults to the root frame.
    :param show: Treeview display mode.
    :return: The created treeview widget.
    """
    frame = frame or self.root
    treeview = ttk.Treeview(frame, columns=columns, show=show)
    for col in columns:
        treeview.heading(col, text=col)
    if style:
        treeview.config(style=style)
    self.widgets['treeview'] = self._add_widget(treeview, row, column, columnspan=columnspan)
    return treeview


def add_tooltip(self, widget_name, text):
    """
    Add a tooltip to a widget.
    
    :param widget_name: Name of the widget to which the tooltip will be added.
    :param text: Tooltip text.
    """
    widget = self.widgets.get(widget_name)
    if widget:
        tooltip = tk.Label(widget, text=text, background="yellow")
        widget.bind("<Enter>", lambda e: tooltip.place(relx=0.5, rely=1.1, anchor="center"))
        widget.bind("<Leave>", lambda e: tooltip.place_forget())

def add_context_menu(self, widget_name, menu_items):
    """
    Add a context menu (right-click menu) to a widget.
    
    :param widget_name: Name of the widget to which the context menu will be added.
    :param menu_items: Dictionary of menu items where keys are item names and values are commands.
    """
    widget = self.widgets.get(widget_name)
    if widget:
        menu = tk.Menu(widget, tearoff=0)
        for item_name, command in menu_items.items():
            menu.add_command(label=item_name, command=command)
        widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

def add_text(self, text, row=None, column=None, columnspan=1, style=None):
    """
    Add a text label to the window.
    
    :param text: The text to display.
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param style: Text label style.
    :return: The created text label widget.
    """
    text_widget = tk.Label(self.root, text=text)
    if style:
        text_widget.config(**style)
    self.widgets['text'] = self._add_widget(text_widget, row, column, columnspan=columnspan)
    return text_widget

def add_listbox(self, items, row=None, column=None, columnspan=1, style=None, frame=None):
    """
    Add a listbox to the window.
    
    :param items: List of items to display in the listbox.
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param style: Listbox style.
    :param frame: The frame to add the listbox to, defaults to the root frame.
    :return: The created listbox widget.
    """
    frame = frame or self.root
    listbox = tk.Listbox(frame)
    for item in items:
        listbox.insert(tk.END, item)
    if style:
        listbox.config(**style)
    self.widgets['listbox'] = self._add_widget(listbox, row, column, columnspan=columnspan)
    return listbox

def add_scrollbar(self, widget_name, orient=tk.VERTICAL, row=None, column=None, rowspan=1, columnspan=1, frame=None):
    """
    Add a scrollbar to a widget.
    
    :param widget_name: Name of the widget to attach the scrollbar to.
    :param orient: Orientation of the scrollbar (VERTICAL or HORIZONTAL).
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :param frame: The frame to add the scrollbar to, defaults to the root frame.
    :return: The created scrollbar widget.
    """
    frame = frame or self.root
    scrollbar = ttk.Scrollbar(frame, orient=orient)
    widget = self.widgets.get(widget_name)
    if widget:
        if orient == tk.VERTICAL:
            widget.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=widget.yview)
        else:
            widget.config(xscrollcommand=scrollbar.set)
            scrollbar.config(command=widget.xview)
    self.widgets['scrollbar'] = self._add_widget(scrollbar, row, column, rowspan=rowspan, columnspan=columnspan)
    return scrollbar

def add_message(self, text, row=None, column=None, columnspan=1, style=None):
    """
    Add a message widget to the window.
    
    :param text: The message text.
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param style: Message widget style.
    :return: The created message widget.
    """
    message = tk.Message(self.root, text=text)
    if style:
        message.config(**style)
    self.widgets['message'] = self._add_widget(message, row, column, columnspan=columnspan)
    return message

def add_paned_window(self, orient=tk.HORIZONTAL, row=None, column=None, rowspan=1, columnspan=1):
    """
    Add a paned window to the window.
    
    :param orient: Orientation of the paned window (HORIZONTAL or VERTICAL).
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :return: The created paned window widget.
    """
    paned_window = ttk.PanedWindow(self.root, orient=orient)
    self.widgets['paned_window'] = self._add_widget(paned_window, row, column, rowspan=rowspan, columnspan=columnspan)
    return paned_window

def add_separator(self, orient=tk.HORIZONTAL, row=None, column=None, columnspan=1):
    """
    Add a separator to the window.
    
    :param orient: Orientation of the separator (HORIZONTAL or VERTICAL).
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :return: The created separator widget.
    """
    separator = ttk.Separator(self.root, orient=orient)
    self.widgets['separator'] = self._add_widget(separator, row, column, columnspan=columnspan)
    return separator

def add_widget(self, widget, row=None, column=None, rowspan=1, columnspan=1):
    """
    Helper function to add a widget to the window using the grid layout.
    
    :param widget: The widget to add.
    :param row: Row position.
    :param column: Column position.
    :param rowspan: Rowspan.
    :param columnspan: Columnspan.
    :return: The added widget.
    """
    widget.grid(row=row if row is not None else self.current_row,
                column=column if column is not None else self.current_column,
                rowspan=rowspan,
                columnspan=columnspan,
                **self.grid_config)
    # Update the current row/column positions for next widget if row/column is not specified
    if row is None:
        self.current_row += 1
    if column is None:
        self.current_column += 1
    return widget

def add_menu(self, menu_structure):
    """
    Add a menu to the window.
    
    :param menu_structure: Dictionary where keys are menu names and values are sub-menu dictionaries.
    :return: The created menu widget.
    """
    menu_bar = tk.Menu(self.root)
    for menu_name, commands in menu_structure.items():
        menu = tk.Menu(menu_bar, tearoff=0)
        for command_name, command in commands.items():
            menu.add_command(label=command_name, command=command)
        menu_bar.add_cascade(label=menu_name, menu=menu)
    self.root.config(menu=menu_bar)
    self.widgets['menu'] = menu_bar
    return menu_bar

def add_menubutton(self, text, menu_items, row=None, column=None, style=None):
    """
    Add a dropdown menu button to the window.
    
    :param text: Text on the menubutton.
    :param menu_items: Dictionary of menu items where keys are item names and values are commands.
    :param row: Row position.
    :param column: Column position.
    :param style: Menubutton style.
    :return: The created menubutton widget.
    """
    menubutton = ttk.Menubutton(self.root, text=text, style='TMenubutton')
    menu = tk.Menu(menubutton, tearoff=0)
    for item_name, command in menu_items.items():
        menu.add_command(label=item_name, command=command)
    menubutton.config(menu=menu)
    if style:
        menubutton.config(**style)
    self.widgets['menubutton'] = self._add_widget(menubutton, row, column)
    return menubutton

def add_text(self, default_text="", width=20, height=5, row=None, column=None, style=None, frame=None):
    """
    Add a multi-line text widget (tk.Text).
    
    :param default_text: Default text for the widget.
    :param width: Width of the widget.
    :param height: Height of the widget.
    :param row: Row position.
    :param column: Column position.
    :param style: Text widget style.
    :param frame: The frame to add the widget to, defaults to the root frame.
    :return: The created text widget.
    """
    frame = frame or self.root
    text_widget = tk.Text(frame, width=width, height=height)
    text_widget.insert(tk.END, default_text)
    if style:
        text_widget.config(**style)
    self.widgets['text'] = self._add_widget(text_widget, row, column)
    return text_widget

def add_option_menu(self, variable, values, row=None, column=None, style=None, frame=None):
    """
    Add an option menu to the window.
    
    :param variable: Tkinter variable associated with the option menu.
    :param values: List of values for the option menu.
    :param row: Row position.
    :param column: Column position.
    :param style: OptionMenu style.
    :param frame: The frame to add the option menu to, defaults to the root frame.
    :return: The created option menu widget.
    """
    frame = frame or self.root
    option_menu = tk.OptionMenu(frame, variable, *values)
    if style:
        option_menu.config(**style)
    self.widgets['option_menu'] = self._add_widget(option_menu, row, column)
    return option_menu

def add_image(self, path, row=None, column=None, columnspan=1, frame=None):
    """
    Add an image to the window using a Label.
    
    :param path: Path to the image file.
    :param row: Row position.
    :param column: Column position.
    :param columnspan: Columnspan.
    :param frame: The frame to add the image to, defaults to the root frame.
    :return: The created image label widget.
    """
    frame = frame or self.root
    img = tk.PhotoImage(file=path)
    label = tk.Label(frame, image=img)
    label.image = img  # Keep a reference to prevent garbage collection
    self.widgets['image'] = self._add_widget(label, row, column, columnspan=columnspan)
    return label

def add_file_dialog(self, dialog_type='open', filetypes=(("All Files", "*.*"),), initialdir="/", title="Select a file"):
    """
    Open a file dialog (open/save).
    
    :param dialog_type: Type of the dialog ('open' or 'save').
    :param filetypes: List of file types to filter.
    :param initialdir: Initial directory.
    :param title: Title of the dialog.
    :return: Selected file path.
    """
    if dialog_type == 'open':
        file_path = filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=filetypes)
    else:
        file_path = filedialog.asksaveasfilename(initialdir=initialdir, title=title, filetypes=filetypes)
    return file_path