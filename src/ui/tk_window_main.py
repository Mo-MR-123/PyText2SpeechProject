from ui.tk_input_box import TkInputBox
from ui.tk_text_label_box import TkTextLabelBox
from tkinter import Tk
from tkinter import ttk

class TkWindowMain:

    def __init__(self, window_title: str):
        self.master = Tk()
        self.master.title(window_title)

        self.configure_tk_style()
        self.configure_ttk_style()
        self.init_widgets()

    def configure_tk_style(self):
        # Configure the background color to metallic black
        self.master.configure(bg='#1C1C1C')

    def configure_ttk_style(self):
        ttk.Style().configure('TFrame', background='#1C1C1C')  
        # ttk.Style().configure("TButton", padding=5, foreground="brown", relief="flat",
        #     background="#ff0000")

    def init_widgets(self):
        # Create and pack the TextBox and InputBox instances
        self.label_box = TkTextLabelBox(self.master, "Test")
        self.label_box.pack(pady=10)

        self.input_box = TkInputBox(self.master, "this is a test input box")
        self.input_box.pack(pady=10)

        # btn = ttk.Button(self.master, text="Click This for testing!", command=self.delete_this_function_testing_only)
        # btn.pack()
    
    def run_mainloop(self):
        self.master.mainloop()
