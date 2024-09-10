from tkinter import Tk
from tkinter import ttk

class TkInputBox(ttk.Frame):

    def __init__(self, master: Tk, label_text: str):
        super().__init__(master)
        self.label = ttk.Label(self, text=label_text)
        self.label.pack(side="left")

        self.entry = ttk.Entry(self)
        self.entry.pack(side="left")
    
    def get_input_text(self) -> str:
        return self.entry.get()