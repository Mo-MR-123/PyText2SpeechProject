from tkinter import Tk 
from tkinter import ttk

class TkTextLabelBox(ttk.Frame):

    def __init__(self, master: Tk, text: str, width: int = None):
        """Initializing a Label Box into a Tk master window.

        Args:
            master (Tk): The parent main window
            text (str): The text to 
            width (int): Width of Label, default None 
            (takes as much width space as possible, might stretch the main Tk window to fit text)
        """
        super().__init__(master)
        self.width = width

        self.label = ttk.Label(self, text=text, width=width, anchor="center", justify="left")
        self.label.pack()
    
    def change_text(self, text):
        # Update the label text
        self.label.config(text=text)

    