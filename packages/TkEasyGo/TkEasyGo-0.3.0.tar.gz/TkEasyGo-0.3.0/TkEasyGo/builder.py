import tkinter as tk
from tkinter import messagebox, filedialog, StringVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class GUIBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Builder")
        self.root.geometry("800x600")  # Set the window size
        self.style = ttk.Style('cosmo')  # You can change 'cosmo' to any other theme

        # Frames for controls, editor, and control list
        self.controls_frame = ttk.Frame(root, bootstyle=PRIMARY)
        self.controls_frame.pack(side="left", fill="y")

        self.editor_frame = ttk.Frame(root, bootstyle=SECONDARY)
        self.editor_frame.pack(side="left", fill="both", expand=True)

        self.property_frame = ttk.Frame(root, bootstyle=PRIMARY)
        self.property_frame.pack(side="right", fill="y")

        # Create Controls, Editor, and Property Editor
        self.create_controls()
        self.create_editor()
        self.create_property_editor()

        # List to store controls and their details
        self.controls = []
        self.current_control = None
        self.highlight = None

    def create_controls(self):
        self.control_types = {
            "Button": ttk.Button,
            "Label": ttk.Label,
            "Entry": ttk.Entry,
            "Checkbutton": ttk.Checkbutton,
            "Radiobutton": ttk.Radiobutton,
            "Listbox": tk.Listbox,
            "Combobox": ttk.Combobox,
            "Spinbox": ttk.Spinbox,
            "Text": tk.Text,
            "Scale": ttk.Scale,
            "Scrollbar": ttk.Scrollbar,
            "Progressbar": ttk.Progressbar,
        }

        # Control type listbox
        self.control_list = tk.Listbox(self.controls_frame, font=('Helvetica', 10), height=12)
        for control in self.control_types:
            self.control_list.insert(tk.END, control)
        self.control_list.pack(padx=10, pady=10)
        self.control_list.bind("<Double-1>", self.add_control)

        # Buttons for additional functionalities
        self.delete_button = ttk.Button(self.controls_frame, text="Delete Control", bootstyle=(DANGER, OUTLINE), command=self.delete_control)
        self.delete_button.pack(padx=10, pady=5)

        self.copy_button = ttk.Button(self.controls_frame, text="Copy Control", bootstyle=(INFO, OUTLINE), command=self.copy_control)
        self.copy_button.pack(padx=10, pady=5)

        self.paste_button = ttk.Button(self.controls_frame, text="Paste Control", bootstyle=(SUCCESS, OUTLINE), command=self.paste_control)
        self.paste_button.pack(padx=10, pady=5)

    def create_editor(self):
        self.canvas = tk.Canvas(self.editor_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.move_control)
        self.canvas.bind("<ButtonRelease-1>", self.release_control)

    def create_property_editor(self):
        self.property_label = ttk.Label(self.property_frame, text="Control Properties", bootstyle=(INFO, INVERSE))
        self.property_label.pack(padx=10, pady=10)

        # Create a container for the property widgets
        self.property_container = ttk.Frame(self.property_frame)
        self.property_container.pack(fill="both", expand=True)

        self.property_widgets = {}

    def clear_property_editor(self):
        if self.property_container:
            self.property_container.destroy()
        self.property_container = ttk.Frame(self.property_frame)
        self.property_container.pack(fill="both", expand=True)
        self.property_widgets.clear()

    def load_properties(self):
        if self.current_control:
            self.clear_property_editor()
            control = self.current_control['control']
            properties = {}

            if isinstance(control, (ttk.Button, ttk.Label, ttk.Checkbutton, ttk.Radiobutton)):
                properties["text"] = {"label": "Text:", "value": control.cget('text')}
            if isinstance(control, (tk.Widget,)):
                properties["bg"] = {"label": "Background:", "value": control.cget('bg') if 'bg' in control.keys() else ''}
            if isinstance(control, (ttk.Entry, tk.Listbox, tk.Text)):
                properties["width"] = {"label": "Width:", "value": control.cget('width') if 'width' in control.keys() else ''}
            if isinstance(control, (tk.Text, tk.Listbox, ttk.Entry)):
                properties["height"] = {"label": "Height:", "value": control.cget('height') if 'height' in control.keys() else ''}
            if isinstance(control, (ttk.Entry, tk.Text, ttk.Label, ttk.Button)):
                properties["font"] = {"label": "Font:", "value": control.cget('font') if 'font' in control.keys() else ''}

            for key, prop in properties.items():
                label = ttk.Label(self.property_container, text=prop["label"])
                label.pack(anchor="w", padx=10)
                if key == "bg":
                    bg_var = StringVar()
                    bg_var.set(prop["value"])
                    combobox = ttk.Combobox(self.property_container, textvariable=bg_var)
                    combobox['values'] = ('white', 'black', 'red', 'green', 'blue', 'yellow', 'gray', 'cyan', 'magenta')
                    combobox.pack(padx=10, fill="x")
                    self.property_widgets[key] = bg_var
                elif key == "font":
                    font_var = StringVar()
                    font_var.set(prop["value"])
                    combobox = ttk.Combobox(self.property_container, textvariable=font_var)
                    combobox['values'] = ('Arial 12', 'Helvetica 12', 'Times New Roman 12', 'Courier 12', 'Comic Sans MS 12', 'Verdana 12', 'Impact 12')
                    combobox.pack(padx=10, fill="x")
                    self.property_widgets[key] = font_var
                else:
                    entry = ttk.Entry(self.property_container)
                    entry.insert(0, prop["value"])
                    entry.pack(padx=10, fill="x")
                    self.property_widgets[key] = entry

            self.update_button = ttk.Button(self.property_container, text="Update", bootstyle=SUCCESS, command=self.update_properties)
            self.update_button.pack(pady=10)
    def update_properties(self):
        if self.current_control:
            control = self.current_control['control']

            # 更新文本属性
            if "text" in self.property_widgets:
                try:
                    control.config(text=self.property_widgets["text"].get())
                except tk.TclError as e:
                    print(f"Error setting text: {e}")

            # 更新背景色属性
            if "bg" in self.property_widgets:
                bg_color = self.property_widgets["bg"].get()
                try:
                    # 检查控件类型，如果是Tkinter基本控件，使用bg，否则使用style
                    if isinstance(control, (tk.Label, tk.Button, tk.Frame, tk.Entry, tk.Text)):
                        control.config(bg=bg_color)
                    elif isinstance(control, (ttk.Label, ttk.Button, ttk.Frame, ttk.Entry)):
                        # 对于 ttk 控件，使用 style 设置背景颜色
                        style = ttk.Style()
                        style_name = f"{control.winfo_class()}.T{control.winfo_class()}"
                        style.configure(style_name, background=bg_color)
                        control.config(style=style_name)
                except tk.TclError as e:
                    print(f"Error setting background color: {e}")

            # 更新宽度属性
            if "width" in self.property_widgets:
                try:
                    control.config(width=int(self.property_widgets["width"].get()))
                except (ValueError, tk.TclError) as e:
                    messagebox.showerror("Invalid Value", "Width must be an integer.")
                    print(f"Error setting width: {e}")

            # 更新高度属性
            if "height" in self.property_widgets:
                try:
                    control.config(height=int(self.property_widgets["height"].get()))
                except (ValueError, tk.TclError) as e:
                    messagebox.showerror("Invalid Value", "Height must be an integer.")
                    print(f"Error setting height: {e}")

            # 更新字体属性
            if "font" in self.property_widgets:
                font_value = self.property_widgets["font"].get()
                if self.is_valid_font(font_value):
                    try:
                        control.config(font=font_value)
                    except tk.TclError as e:
                        messagebox.showerror("Invalid Font", "Unable to apply the specified font.")
                        print(f"Error setting font: {e}")
                else:
                    messagebox.showerror("Invalid Font", "Font value must be in 'family size style' format (e.g., 'Arial 12 bold').")

    def is_valid_font(self, font):
        try:
            import tkinter.font as tkFont
            tkFont.Font(font=font)  # 尝试创建一个Font对象以验证字体
            return True
        except tk.TclError:
            return False


    def add_control(self, event):
        selection = self.control_list.curselection()
        if not selection:
            return
        control_type = self.control_list.get(selection[0])
        if control_type:
            control_class = self.control_types[control_type]
            x, y = 10, 10
            
            if control_class in [tk.Button, tk.Label, tk.Checkbutton, tk.Radiobutton]:
                control = control_class(self.canvas, text=control_type)
            else:
                control = control_class(self.canvas)
                
            window = self.canvas.create_window(x, y, window=control, anchor="nw")
            name = self.get_unique_name(control_type.lower())
            self.controls.append({'name': name, 'type': control_type, 'window': window, 'control': control, 'position': (x, y)})
            self.add_control_to_list(name)
    
    def move_control(self, event):
        if not self.current_control:
            return

        # 计算新的坐标
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        # 更新画布上控件的位置
        self.canvas.coords(self.current_control['window'], x, y)
        
        # 更新控件的存储位置
        self.current_control['position'] = (x, y)

        # 重新绘制高亮边框
        if self.highlight:
            self.canvas.delete(self.highlight)
        x0, y0, x1, y1 = self.canvas.bbox(self.current_control['window'])
        self.highlight = self.canvas.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2, outline="blue", width=2)

    
    def on_canvas_click(self, event):
        clicked_item = self.canvas.find_closest(event.x, event.y)
        if clicked_item:
            self.current_control = next((ctrl for ctrl in self.controls if ctrl['window'] == clicked_item[0]), None)
            if self.current_control:
                self.load_properties()
                self.highlight_control()
                self.highlight_control_in_list()

    def highlight_control(self):
        if self.highlight:
            self.canvas.delete(self.highlight)

        x0, y0, x1, y1 = self.canvas.bbox(self.current_control['window'])
        self.highlight = self.canvas.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2, outline="blue", width=2)

    def highlight_control_in_list(self):
        if self.current_control:
            index = self.added_controls_list.get(0, tk.END).index(self.current_control['name'])
            self.added_controls_list.selection_clear(0, tk.END)
            self.added_controls_list.selection_set(index)

    def release_control(self, event):
        self.current_control = None

    def get_unique_name(self, base_name):
        existing_names = [ctrl['name'] for ctrl in self.controls]
        counter = 1
        unique_name = f"{base_name}{counter}"
        while unique_name in existing_names:
            counter += 1
            unique_name = f"{base_name}{counter}"
        return unique_name

    def add_control_to_list(self, name):
        if not hasattr(self, 'added_controls_list'):
            self.added_controls_list = tk.Listbox(self.property_frame)
            self.added_controls_list.pack(padx=10, pady=10)
            self.added_controls_list.bind("<<ListboxSelect>>", self.on_control_select)

        self.added_controls_list.insert(tk.END, name)
    
    def refresh_control_list(self):
        self.added_controls_list.delete(0, tk.END)
        for ctrl in self.controls:
            self.added_controls_list.insert(tk.END, ctrl['name'])

    def on_control_select(self, event):
        selection = self.added_controls_list.curselection()
        if selection:
            selected_name = self.added_controls_list.get(selection[0])
            self.current_control = next(ctrl for ctrl in self.controls if ctrl['name'] == selected_name)
            self.load_properties()
            self.highlight_control()

    def copy_control(self):
        if self.current_control:
            control_widget = self.current_control['control']
            
            # Create a dictionary to hold the copied control's attributes
            clipboard_attributes = {
                'type': self.current_control['type'],
                'position': self.current_control['position'],
                'control': {}
            }
            
            # Check and copy the 'text' attribute
            if 'text' in control_widget.keys():
                clipboard_attributes['control']['text'] = control_widget.cget('text')
            
            # Check and copy the 'bg' attribute (or 'background' as alternative)
            if 'bg' in control_widget.keys():
                clipboard_attributes['control']['bg'] = control_widget.cget('bg')
            elif 'background' in control_widget.keys():
                clipboard_attributes['control']['bg'] = control_widget.cget('background')
            
            # Check and copy the 'width' attribute
            if 'width' in control_widget.keys():
                clipboard_attributes['control']['width'] = control_widget.cget('width')
            
            # Check and copy the 'height' attribute
            if 'height' in control_widget.keys():
                clipboard_attributes['control']['height'] = control_widget.cget('height')
            
            # Check and copy the 'font' attribute
            if 'font' in control_widget.keys():
                clipboard_attributes['control']['font'] = control_widget.cget('font')
            
            # Store the copied attributes in the clipboard
            self.clipboard_control = clipboard_attributes
            
            messagebox.showinfo("Info", "Control copied to clipboard")


    def paste_control(self):
        if hasattr(self, 'clipboard_control'):
            control_data = self.clipboard_control
            x, y = 10, 10
            control_class = self.control_types[control_data['type']]
            
            # Create a dictionary to hold keyword arguments
            kwargs = {}

            # Check and set the 'text' attribute
            if 'text' in control_data['control']:
                kwargs['text'] = control_data['control']['text']

            # Check and set the 'bg' attribute (only for widgets that support it)
            if 'bg' in control_data['control']:
                if hasattr(control_class, 'configure') and 'background' in control_class().configure():
                    kwargs['background'] = control_data['control']['bg']
                elif hasattr(control_class, 'configure') and 'bg' in control_class().configure():
                    kwargs['bg'] = control_data['control']['bg']

            # Check and set the 'width' attribute (only for widgets that support it)
            if 'width' in control_data['control']:
                if hasattr(control_class, 'configure') and 'width' in control_class().configure():
                    kwargs['width'] = control_data['control']['width']

            # Check and set the 'height' attribute (only for widgets that support it)
            if 'height' in control_data['control']:
                if hasattr(control_class, 'configure') and 'height' in control_class().configure():
                    kwargs['height'] = control_data['control']['height']

            # Check and set the 'font' attribute (only for widgets that support it)
            if 'font' in control_data['control']:
                if hasattr(control_class, 'configure') and 'font' in control_class().configure():
                    kwargs['font'] = control_data['control']['font']

            # Create a new control using the safe kwargs
            control = control_class(self.canvas, **kwargs)
            
            # Place the new control on the canvas
            window = self.canvas.create_window(x, y, window=control, anchor="nw")
            name = self.get_unique_name(control_data['type'].lower())
            self.controls.append({'name': name, 'type': control_data['type'], 'window': window, 'control': control, 'position': (x, y)})
            self.add_control_to_list(name)
            messagebox.showinfo("Info", "Control pasted")



    def delete_control(self):
        if self.current_control:
            # 删除画布上的控件
            self.canvas.delete(self.current_control['window'])
            # 从控件列表中移除
            self.controls.remove(self.current_control)
            # 刷新控件列表
            self.refresh_control_list()
            # 清除属性编辑器
            self.clear_property_editor()
            # 清除当前控件和高亮显示
            self.current_control = None
            if self.highlight:
                self.canvas.delete(self.highlight)
                self.highlight = None

    def generate_code(self):
        code = "import tkinter as tk\n"
        code += "from tkinter import ttk\n\n"
        code += "root = tk.Tk()\n\n"
        
        for control in self.controls:
            control_type = control['type']
            x, y = control['position']
            name = control['name']
            
            # 获取控件的属性值
            text = control['control'].cget('text') if 'text' in control['control'].keys() else ''
            bg = control['control'].cget('bg') if 'bg' in control['control'].keys() else ''
            width = control['control'].cget('width') if 'width' in control['control'].keys() else ''
            height = control['control'].cget('height') if 'height' in control['control'].keys() else ''
            font = control['control'].cget('font') if 'font' in control['control'].keys() else ''
            
            # 根据控件类型选择前缀
            if control_type in ["Combobox", "Progressbar"]:  # 使用ttk的控件
                prefix = "ttk."
            else:
                prefix = "tk."
            
            # 构建控件的创建行
            code_line = f"{name} = {prefix}{control_type}(root"
            
            if text:
                code_line += f", text='{text}'"
            if bg:
                code_line += f", bg='{bg}'"
            if width:
                code_line += f", width={width}"
            if height:
                code_line += f", height={height}"
            if font:
                code_line += f", font='{font}'"
            
            # 关闭括号并换行
            code_line += ")\n"
            
            # 添加控件的布局信息
            code_line += f"{name}.place(x={x}, y={y})\n"
            
            # 添加到代码中
            code += code_line + "\n"
        
        code += "root.mainloop()\n"
        return code

    def save_code(self):
        code = self.generate_code()
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(code)
            messagebox.showinfo("Info", f"Code saved as {file_path}")

    def show_save_button(self):
        save_button = tk.Button(self.root, text="Save Code", command=self.save_code)
        save_button.pack(padx=10, pady=10)

    @staticmethod
    def run():
        root = tk.Tk()
        app = GUIBuilder(root)
        app.show_save_button()
        root.mainloop()
