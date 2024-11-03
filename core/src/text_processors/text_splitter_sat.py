import torch
import gc

from wtpsplit import SaT
from typing import List

class TextSplitterSaT:

    def __init__(self, lang: str, style_or_domain: str, sat_model_name: str = "sat-12l-sm"):
        self.lang = lang
        self.sat_model_name = sat_model_name
        self.style_or_domain = style_or_domain

        # Check if CUDA is available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Init model (first run will download the model so takes a while)
        self.sat = SaT(self.sat_model_name, style_or_domain=self.sat_model_name, language=self.lang)
        
        if new_device == "cpu":
            self.sat.to(new_device)    
        elif new_device == "cuda":
            self.sat.half().to(new_device)

    def split_str_in_sentences(self, string_to_split: str) -> List[str]:
        return list(self.sat.split(string_to_split))

    def eject_model(self):
        # Move model to CPU
        self.sat.model.model.cpu()
        self.sat.model.cpu()
        self.sat.cpu()

        # Delete model
        del self.sat.model.model 
        del self.sat.model
        del self.sat.tokenizer
        del self.sat

        torch.cuda.empty_cache()

        gc.collect()

    def reinit_model(self):
        self.eject_model()

        self.sat = SaT(self.sat_model_name, style_or_domain=self.sat_model_name, language=self.lang)
        self.sat.half().to(self.device)

    def change_device(self, new_device):
        if new_device in ["cpu", "cuda"]:
            self.device = new_device

        if self.sat:
            if new_device == "cpu":
                self.sat.to(new_device)    
            elif new_device == "cuda":
                self.sat.half().to(new_device)
        
    def change_lang(self, new_lang: str):
        self.lang = new_lang
        self.reinit_model()

    def change_style_or_domain(self, new_style_or_domain: str):
        self.style_or_domain = style_or_domain
        self.reinit_model()

    def change_sat_model_name(self, new_sat_model_name: str):
        self.sat_model_name = new_sat_model_name
        self.reinit_model()


