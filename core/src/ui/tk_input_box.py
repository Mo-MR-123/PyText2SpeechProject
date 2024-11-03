import customtkinter as ctk

class TkInputBox(ctk.CTkFrame):

    def __init__(self, master: ctk.CTk, label_text: str):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.pack(side="left")

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(padx=5, side="left")
    
    def get_input_text(self) -> str:
        return self.entry.get()