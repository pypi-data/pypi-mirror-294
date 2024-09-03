# moudule/utils.py

def bind_event(self, widget_name, event_name, handler):
    """
    Bind an event handler to a specific event on a widget.
    
    :param widget_name: The name of the widget (retrieved from the widgets dictionary).
    :param event_name: The name of the event (e.g., "<Button-1>").
    :param handler: The event handler function.
    """
    widget = self.widgets.get(widget_name)
    if widget:
        widget.bind(event_name, handler)

def bind_events(self, widget_name, events):
    """
    Bind multiple event handlers to multiple events on a widget.
    
    :param widget_name: The name of the widget (retrieved from the widgets dictionary).
    :param events: A dictionary of event names and their corresponding handlers.
    """
    widget = self.widgets.get(widget_name)
    if widget:
        for event_name, handler in events.items():
            widget.bind(event_name, handler)

def disable_widget(self, widget_name):
    """
    Disable a specified widget, making it unusable.
    
    :param widget_name: The name of the widget (retrieved from the widgets dictionary).
    """
    widget = self.widgets.get(widget_name)
    if widget:
        widget.state(["disabled"])

def enable_widget(self, widget_name):
    """
    Enable a specified widget, making it usable.
    
    :param widget_name: The name of the widget (retrieved from the widgets dictionary).
    """
    widget = self.widgets.get(widget_name)
    if widget:
        widget.state(["!disabled"])

def remove_widget(self, widget_name):
    """
    Remove a specified widget from the window and destroy it.
    
    :param widget_name: The name of the widget (retrieved from the widgets dictionary).
    """
    widget = self.widgets.pop(widget_name, None)
    if widget:
        widget.grid_forget()  # Remove widget from the grid layout
        widget.destroy()      # Destroy the widget
