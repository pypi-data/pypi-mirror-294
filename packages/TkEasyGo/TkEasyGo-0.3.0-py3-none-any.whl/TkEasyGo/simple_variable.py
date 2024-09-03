import tkinter as tk
from typing import Callable, Optional, Union

class SimpleVariable:
    """
    A simple wrapper around Tkinter's Variable classes with additional utility methods for easier use.

    This class simplifies the use of Tkinter's StringVar, IntVar, DoubleVar, and BooleanVar,
    adding utility methods that make it more convenient to work with variable tracing,
    and different data types such as integers, floats, or booleans.
    
    Attributes:
        var (tk.Variable): The underlying Tkinter Variable instance.
        initial_value: The initial value of the variable.
    """

    def __init__(self, initial_value: Optional[Union[str, int, float, bool]] = None, var_type: Optional[type] = None):
        """
        Initialize the SimpleVariable instance.

        Args:
            initial_value (Optional[Union[str, int, float, bool]]): The initial value for the Variable.
            var_type (Optional[type]): The Tkinter variable type to use (StringVar, IntVar, DoubleVar, BooleanVar).
                                       If not provided, the type will be inferred from the initial_value.
        """
        if var_type is None:
            if isinstance(initial_value, int):
                self.var = tk.IntVar(value=initial_value)
            elif isinstance(initial_value, float):
                self.var = tk.DoubleVar(value=initial_value)
            elif isinstance(initial_value, bool):
                self.var = tk.BooleanVar(value=initial_value)
            else:
                self.var = tk.StringVar(value=initial_value)
        else:
            self.var = var_type(value=initial_value)
        
        self.initial_value = initial_value

    def get(self) -> Union[str, int, float, bool]:
        """
        Get the current value of the variable.

        Returns:
            Union[str, int, float, bool]: The current value stored in the Tkinter Variable.
        """
        return self.var.get()

    def set(self, value: Union[str, int, float, bool]):
        """
        Set the value of the variable.

        Args:
            value (Union[str, int, float, bool]): The value to set in the Tkinter Variable.
        """
        self.var.set(value)

    def trace(self, callback: Callable[[str], None], mode: str = "write"):
        """
        Attach a callback to be triggered whenever the variable's value changes.

        The callback will be passed the new value of the variable as its argument.

        Args:
            callback (Callable[[str], None]): The function to call when the variable changes.
            mode (str): The trace mode, either 'write', 'read', or 'unset'. Default is 'write'.
        """
        self.var.trace_add(mode, lambda *args: callback(self.get()))

    def untrace(self, mode: str = "write"):
        """
        Remove all callbacks associated with the specified trace mode.

        Args:
            mode (str): The trace mode to remove callbacks from. Default is 'write'.
        """
        self.var.trace_remove(mode)

    def bind_to_widget(self, widget: tk.Widget, attribute: str = "text"):
        """
        Bind the variable to a widget's attribute (e.g., text, value) for automatic updates.

        Args:
            widget (tk.Widget): The widget to bind the variable to.
            attribute (str): The widget attribute to bind to (default is "text").

        Raises:
            AttributeError: If the widget does not have the specified attribute.
        """
        if hasattr(widget, attribute):
            widget.config(textvariable=self.var)
        else:
            raise AttributeError(f"The widget does not have the attribute '{attribute}'.")

    def get_as_int(self) -> int:
        """
        Get the variable's value as an integer.

        Returns:
            int: The integer value of the variable.

        Raises:
            ValueError: If the current value cannot be converted to an integer.
        """
        try:
            return int(self.get())
        except ValueError:
            raise ValueError("The current value cannot be converted to an integer.")

    def get_as_float(self) -> float:
        """
        Get the variable's value as a float.

        Returns:
            float: The float value of the variable.

        Raises:
            ValueError: If the current value cannot be converted to a float.
        """
        try:
            return float(self.get())
        except ValueError:
            raise ValueError("The current value cannot be converted to a float.")

    def get_as_bool(self) -> bool:
        """
        Get the variable's value as a boolean.

        The conversion follows standard Python truthiness rules.

        Returns:
            bool: The boolean value of the variable.
        """
        return bool(self.get())

    def increment(self, step: int = 1):
        """
        Increment the variable's value by a given step.

        This method assumes the current value is an integer.

        Args:
            step (int): The amount to increment by (default is 1).

        Raises:
            ValueError: If the current value cannot be converted to an integer.
        """
        try:
            current_value = self.get_as_int()
            self.set(current_value + step)
        except ValueError:
            raise ValueError("The current value is not an integer and cannot be incremented.")

    def decrement(self, step: int = 1):
        """
        Decrement the variable's value by a given step.

        This method assumes the current value is an integer.

        Args:
            step (int): The amount to decrement by (default is 1).

        Raises:
            ValueError: If the current value cannot be converted to an integer.
        """
        self.increment(-step)

    def reset(self, value: Optional[Union[str, int, float, bool]] = None):
        """
        Reset the variable to a specified value, or to its initial value if none is provided.

        Args:
            value (Optional[Union[str, int, float, bool]]): The value to reset to. If not provided, the initial value will be used.
        """
        if value is None:
            value = self.initial_value
        self.set(value)

    def clear(self):
        """
        Clear the value of the variable, setting it to an empty string (or zero for numeric types).
        """
        if isinstance(self.var, (tk.IntVar, tk.DoubleVar)):
            self.set(0)
        elif isinstance(self.var, tk.BooleanVar):
            self.set(False)
        else:
            self.set("")

    def trigger_event(self):
        """
        Manually trigger a write event for the variable's trace callbacks.
        """
        self.var.set(self.var.get())

