
# TkEasyGo

**TkEasyGo** 是一个简单的跨平台 GUI 生成器，旨在帮助开发者快速创建基本的图形用户界面。它基于 `tkinter` 实现，并提供了一系列基本控件和功能，使用户能够轻松构建简单的应用界面。

[English](README_EN.md)

## 文件结构

├── docs
│   ├── contact.md                # 联系信息
│   ├── contributing.md           # 贡献指南
│   ├── controls.md               # 控件使用指南
│   ├── docs.md                   # 项目文档概述
│   ├── event_binding.md          # 事件绑定的详细说明
│   ├── faq.md                    # 常见问题解答
│   ├── getting_started.md        # 快速入门指南
│   ├── installation.md           # 安装指南
│   ├── license.md                # 许可证详细信息
│   ├── README.md                 # 文档首页
│   ├── styling.md                # 样式和主题设置指南
│   └── window_operations.md      # 窗口操作指南
├── examples
│   ├── Combobox_app.py           # 示例：展示如何使用下拉框控件（Combobox）
│   ├── event_app.py              # 示例：演示如何处理事件
│   ├── label_app.py              # 示例：展示如何使用标签控件（Label）
│   ├── layout_app.py             # 示例：展示如何使用不同的布局管理功能
│   ├── notebook_Slider_app.py    # 示例：展示如何使用选项卡控件（Notebook）和滑块控件（Slider）
│   ├── paned_window_test.py      # 示例：展示如何使用 PanedWindow 控件
│   ├── Progressbar_app.py        # 示例：展示如何使用进度条控件（Progressbar）
│   ├── scrollbar_test.py         # 示例：展示如何使用滚动条控件（Scrollbar）
│   ├── separator_test.py         # 示例：展示如何使用分隔符控件（Separator）
│   ├── spinbox_test.py           # 示例：展示如何使用数字输入框控件（Spinbox）
│   ├── tabbed_app.py             # 示例：展示如何使用选项卡（Tabbed）控件
│   |── treeview_test.py          # 示例：展示如何使用树视图控件（Treeview）
|   └── test_components.py        # 示例：日历控件、颜色选择器、文件选择器、警告框等
├── LICENSE                       # 项目许可证文件，详细信息请参见
├── README.md                     # 项目说明文件
├── setup.py                      # 安装脚本，包含库的依赖和安装设置
├── test.ipynb                    # 测试和实验的 Jupyter Notebook 文件
├── tests
│   └── test_core.py              # 用于测试核心功能的测试文件
└── TkEasyGo
    ├── core.py                   # 核心实现文件，定义主要的控件和窗口管理功能
    ├── events.py                 # 事件处理功能实现
    ├── layout.py                 # 布局管理功能实现
    ├── platform.py               # 平台相关的功能实现
    ├── simple_variable.py        # 简单的变量管理功能
    ├── simple_window.py          # 简单窗口的实现，集成各种控件和布局
    ├── themes.py                 # 主题和样式管理功能实现
    ├── __init__.py               # 库的初始化文件
    |── module                    # 模块文件夹
    └── __pycache__               # 编译的 Python 字节码文件
        ├── core.cpython-310.pyc
        ├── events.cpython-310.pyc
        ├── layout.cpython-310.pyc
        ├── platform.cpython-310.pyc
        ├── simple_variable.cpython-310.pyc
        ├── simple_window.cpython-310.pyc
        └── themes.cpython-310.pyc



## 目前支持的功能

- **标签** (`Label`): 显示静态文本。
- **按钮** (`Button`): 触发事件的按钮。
- **文本框** (`Textbox`): 用于输入和显示文本。
- **复选框** (`Checkbox`): 允许用户选择或取消选择一个选项。
- **单选按钮** (`Radiobutton`): 允许用户在多个选项中选择一个。
- **下拉框** (`Combobox`): 提供一个下拉列表供用户选择。
- **进度条** (`Progressbar`): 显示进度的可视化控件。
- **滑块** (`Slider`): 用于在数值范围内选择值。
- **选项卡** (`Notebook`): 提供多个标签页以组织内容。
- **帧** (`Frame`): 用于组织和分组其他控件。

## 未来计划

- **增强主题支持**: 引入更多的主题和样式选项，以提升界面的美观性和用户体验。
- **增加更多控件**: 如日历控件、图表控件等，以满足更复杂的应用需求。
- **改进布局管理**: 提供更灵活的布局选项，使用户可以更自由地安排控件的位置和大小。
- **提高性能**: 优化控件的性能，确保在大型应用中依然流畅。

## 待办事项

- **用户文档**: 完善用户手册和开发文档，以帮助用户更好地使用库。
- **示例应用**: 提供更多示例应用和教程，以展示库的不同用法和功能。
- **错误修复**: 持续修复已知的 bug 和问题，以提升库的稳定性。
- **社区支持**: 建立社区支持渠道，收集用户反馈并及时响应。

# TkEasyGo 使用教程

**TkEasyGo** 是一个简化的跨平台 GUI 生成器，基于 `tkinter` 实现，旨在帮助开发者快速创建图形用户界面。本文将介绍如何安装和使用 TkEasyGo，展示一些常见的用法示例，并提供一些技巧和注意事项。

## 安装

要安装 TkEasyGo，可以使用 `pip` 从 PyPI 安装：

```sh
pip install TkEasyGo
```

## 快速入门

### 创建一个基本的窗口

下面的示例展示了如何创建一个简单的窗口，并添加一些基本控件：

```python
from TkEasyGo.core import SimpleWindow, SimpleVariable

def basic_app():
    # 创建窗口
    window = SimpleWindow(title="Basic TkEasyGo App", width=300, height=200)
    
    # 添加标签
    window.add_label("Welcome to TkEasyGo!", row=0, column=0, columnspan=2)
    
    # 添加文本框
    textbox = window.add_textbox("Type here...", row=1, column=0, columnspan=2)
    
    # 添加按钮
    button = window.add_button("Submit", lambda: print("Submit clicked"), row=2, column=0, columnspan=2)
    
    # 添加复选框
    checkbox_var = SimpleVariable()
    window.add_checkbox("Check me", checkbox_var, row=3, column=0)
    
    # 运行窗口
    window.run()

if __name__ == "__main__":
    basic_app()
```

### 控件介绍

#### 标签 (`Label`)

用于显示静态文本。可以通过 `add_label` 方法添加。

```python
window.add_label("This is a label", row=0, column=0)
```

#### 按钮 (`Button`)

用于触发事件。可以通过 `add_button` 方法添加。

```python
window.add_button("Click Me", lambda: print("Button clicked"), row=1, column=0)
```

#### 文本框 (`Textbox`)

用于输入和显示文本。可以通过 `add_textbox` 方法添加。

```python
textbox = window.add_textbox("Default text", row=2, column=0)
```

#### 复选框 (`Checkbox`)

允许用户选择或取消选择一个选项。可以通过 `add_checkbox` 方法添加。

```python
checkbox_var = SimpleVariable()
window.add_checkbox("Check me", checkbox_var, row=3, column=0)
```

#### 单选按钮 (`Radiobutton`)

允许用户在多个选项中选择一个。可以通过 `add_radiobutton` 方法添加。

```python
radiobutton_var = SimpleVariable("1")
window.add_radiobutton("Option 1", "1", radiobutton_var, row=4, column=0)
```

#### 下拉框 (`Combobox`)

提供一个下拉列表供用户选择。可以通过 `add_combobox` 方法添加。

```python
combobox = window.add_combobox(["Option 1", "Option 2", "Option 3"], row=5, column=0)
```

#### 进度条 (`Progressbar`)

显示进度的可视化控件。可以通过 `add_progressbar` 方法添加。

```python
progressbar = window.add_progressbar(value=50, row=6, column=0, columnspan=2)
```

#### 滑块 (`Slider`)

用于在数值范围内选择值。可以通过 `add_slider` 方法添加。

```python
slider = window.add_slider(value=50, row=7, column=0, columnspan=2)
```

#### 选项卡 (`Notebook`)

提供多个标签页以组织内容。可以通过 `add_notebook` 方法添加。

```python
def tab1_content(window, frame):
    window.add_label("This is Tab 1", row=0, column=0, frame=frame)
    window.add_button("Button in Tab 1", lambda: print("Tab 1 Button clicked"), row=1, column=0, frame=frame)

def tab2_content(window, frame):
    window.add_label("This is Tab 2", row=0, column=0, frame=frame)
    window.add_button("Button in Tab 2", lambda: print("Tab 2 Button clicked"), row=1, column=0, frame=frame)

window.add_notebook({"Tab 1": tab1_content, "Tab 2": tab2_content}, row=8, column=0, columnspan=2)
```

## 事件绑定

可以通过 `bind_event` 方法为控件绑定事件：

```python
window.bind_event('textbox', '<KeyRelease>', lambda event: print(f"Text changed to: {textbox.get()}"))
window.bind_event('button', '<Button-1>', lambda event: print("

Button clicked"))
```

## 窗口操作

### 设置窗口的最小化、最大化和恢复功能

`SimpleWindow` 提供了窗口操作的方法，包括最小化、最大化和恢复：

- **最大化**: 使用 `maximize()` 方法将窗口切换到全屏模式。
- **最小化**: 使用 `minimize()` 方法将窗口最小化到任务栏。
- **恢复**: 使用 `restore()` 方法将窗口恢复到原始大小。

示例代码如下：

```python
def window_operations_app():
    window = SimpleWindow(title="Window Operations App", width=400, height=300)
    
    # 添加操作按钮
    window.add_button("Maximize", window.maximize, row=0, column=0)
    window.add_button("Minimize", window.minimize, row=1, column=0)
    window.add_button("Restore", window.restore, row=2, column=0)
    
    # 运行窗口
    window.run()

if __name__ == "__main__":
    window_operations_app()
```

## 常见问题

### 如何调整控件的样式？

你可以在 `SimpleWindow` 的 `configure_styles` 方法中配置控件的样式。例如：

```python
window.configure_styles('TButton', padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
```

### 如何贡献代码？

如果你希望为 TkEasyGo 做出贡献，可以通过 GitHub 提交 Pull Request，或者报告问题和建议。我们欢迎任何形式的贡献。

## 联系我们

- **电子邮件**: tkeasygo@gmail.com
- **GitHub**: [https://github.com/TkEasyGo/TkEasyGo](https://github.com//TkEasyGo)

## 许可证

本项目使用 MIT 许可证，详细信息请参见 [LICENSE](LICENSE) 文件。
