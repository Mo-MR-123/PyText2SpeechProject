import torch
import customtkinter as ctk
import tkinter as tk

from TTS.api import TTS
from pathlib import Path
from tkinter import filedialog, messagebox
# from ui.tk_text_label_box import TkTextLabelBox
from ui.tk_input_box import TkInputBox
from src.parsers.pymupdf_parser import PyMuPDFParser
from src.text_processors.pre_processor import PreProcessor
from src.text_processors.text_splitter_sat import TextSplitterSaT

"""
The following code is partially inspired by 
https://github.com/lukaszliniewicz/Pandrator 
"""
class TkWindowMain(ctk.CTk):

    def __init__(self, window_title: str, width_factor: float = 0.5, height_factor: float = 0.5):
        # Init some prerequists:
        # 1) Init preprocessor for processing text before passing to to tts model (for better quality)
        # 2) Check if CUDA is available
        self.preprocessor = PreProcessor()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Init CTk instance
        self.master = ctk.CTk()
        self.master.title("Text To Speech XTTSv2 App")

        assert width_factor > 0 and width_factor <= 1, f"given width_factor is {width_factor} is not between 0 and 1."
        assert height_factor > 0 and height_factor <= 1, f"given height_factor is {height_factor} is not between 0 and 1."

        # Layout
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Screen resolution
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.window_width = int(screen_width * width_factor)
        self.window_height = int(screen_height * height_factor)

        # Configuring main window properties
        self.master.title(window_title)
        self.master.geometry(f"{self.window_width}x{self.window_height}")
        self.master.minsize(self.window_width, self.window_height)
        self.master.maxsize(self.window_width, self.window_height)

        # Default Configs for certain Widgets
        self.default_label_font = ctk.CTkFont(size=14, weight="bold")
        self.default_pady = 10
        self.default_padx = 10

        # Create variables to hold the state of the checkboxes of Lang selection
        self.check_var_en = ctk.IntVar(value=0)
        self.check_var_nl = ctk.IntVar(value=0)

        self.selected_file_txt = ""
        self.supported_file_suffixes = [".xps",".mobi",".fb2",".cbz",".txt",".pdf",".epub"]

        self.init_widgets()
    
    def init_tts_model(self):
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(dev)

    def is_filetype_supported(self, file_suffix: str) -> bool:
        return file_suffix in self.supported_file_suffixes 

    def preprocess_selected_txt(self):
        pass # TODO:

    def select_file_for_speech_conversion(self) -> None:
        selected_file_path = \
            filedialog.askopenfilename(
                title="Select File To Convert To Speech",  # Set a custom title for the file dialog
                filetypes=[
                    ("Text, PDF, XPS, MOBI, FB2, CBZ and EPUB files", "*.xps *.mobi *.fb2 *.cbz *.txt *.pdf *.epub"),
                    # ("All files", "*.*")
                ]
            )

        if selected_file_path:
            selected_file_path = Path(selected_file_path)
            if self.is_filetype_supported(selected_file_path.suffix):
                # TODO: more memory efficient to open handle to file and read 
                #       each page during conversion only instead of loading
                #       all the text at once. Make sure to close handle when
                #       the app is closed using event to capture closing of tk window.
                with PyMuPDFParser(selected_file_path) as f: 
                    self.selected_file_txt = f.extract_all_text()
                    # TODO: preprocess text here... 
            else:
                messagebox.showerror("Unsupported File Type", f"The file type '{selected_file_path.suffix}' is not supported.")

    def on_lang_checkbutton_change(self, checkbox_number):
        if checkbox_number == 1:
            if self.check_var_nl.get() == 1:
                self.check_var_en.set(0)  # Uncheck checkbox 2 if checkbox 1 is checked
        elif checkbox_number == 2:
            if self.check_var_en.get() == 1:
                self.check_var_nl.set(0)  # Uncheck checkbox 1 if checkbox 2 is checked

    def init_widgets(self):
        # Create the main scrollable frame where all widgets will reside
        main_scrollable_frame_height = int(self.window_height * 0.90)
        main_scrollable_frame_width = int(self.window_width * 0.95)
        self.main_scrollable_frame = ctk.CTkScrollableFrame(
            self.master, 
            width=main_scrollable_frame_width, 
            height=main_scrollable_frame_height
        )
        self.main_scrollable_frame.grid(
            row=0, 
            column=0, 
            padx=self.default_padx, 
            pady=self.default_pady, 
            sticky=tk.NSEW
        )
        self.main_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.main_scrollable_frame.grid_rowconfigure(0, weight=1)

        # Create and pack the TextBox and InputBox instances
        # self.first_label = ttk.Label(self.master, text="First label", anchor="center", justify="left")
        self.first_label = ctk.CTkLabel(
            self.main_scrollable_frame, 
            text="Select Spoken Speech Language:", 
            font=self.default_label_font
        )
        self.first_label.pack(pady=5)

        # Create the first checkbox
        self.checkbox_nl = ctk.CTkCheckBox(
            self.main_scrollable_frame, 
            text="Dutch", 
            variable=self.check_var_nl, 
            command=lambda: self.on_lang_checkbutton_change(1)
        )
        self.checkbox_nl.pack(pady=self.default_pady)

        # Create the second checkbox
        self.checkbox_en = ctk.CTkCheckBox(
            self.main_scrollable_frame, 
            text="English", 
            variable=self.check_var_en, 
            command=lambda: self.on_lang_checkbutton_change(2)
        )
        self.checkbox_en.pack(pady=self.default_pady)

        self.first_label = ctk.CTkLabel(
            self.main_scrollable_frame, 
            text="Select File To Convert To Speech", 
            font=self.default_label_font
        )
        self.first_label.pack(pady=5)

        self.browse_btn = ctk.CTkButton(
            self.main_scrollable_frame, 
            text="Select file", 
            command=self.select_file_for_speech_conversion
        )
        self.browse_btn.pack(pady=self.default_pady)

        # for _ in range(20):
        #     btn = ctk.CTkButton(self.main_scrollable_frame, text="Click This for testing!", command=None)
        #     btn.pack(pady=self.default_pady)
    
    def run_mainloop(self):
        self.master.mainloop()
