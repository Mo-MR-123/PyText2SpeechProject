import logging
import string
import re

from typing import List
from core.loggers.log_config import LogConfig

log_config = LogConfig(log_level=logging.DEBUG)

"""
Pre-Processor for text generated by parsers
"""
class PreProcessor:

    def __init__(self):
        self.logger = log_config.get_logger(self.__class__.__name__)

    def remove_unwanted_nonascii_chars(self, text_str: str):
        return text_str \
            .replace("\r", " ") \
            .replace("\n", " ") \
            .replace("\t", " ") \
            .replace("\x0c", " ") \
            .replace("\xa0", " ") \
            .replace("\xad", " ")

    def remove_punctuations(self, text_str: str) -> str:
        """
        This function remove punctuations in a string.

        Args:
            text_str (str): A string to remove punctuations from.

        Returns:
            str: The same string/sentence without punctuations.
        """
        # Create a translation table that maps each punctuation character to None
        translator = str.maketrans('', '', string.punctuation+"‘"+"’")

        # Use the translate method to remove all punctuation
        return text_str.translate(translator)

    def remove_punctuations_at_end(self, text_str: str) -> str:
        """
        This function remove a subset of common punctuations at the end of a sentence/string.
        Punctuations to be removed: '.' && ',' && '!' && '?' &&  ';' && ':'

        Args:
            text_str (str): A string from which punctuations at the end need to be removed.

        Returns:
            str: The same string/sentence without punctuations at the end.
        """

        # rstrip will continue to remove each char separately from text from the right
        # until it doesn't encounter one anymore (from the right).
        return text_str.rstrip('.,!?;:')

    def remove_ref_numbers(self, text_str: str) -> str:
        """
        This function remove reference numbers (if applicable) from a sentence/string.
        Examples of reference numbers: 
            1) "Research showed increase in population.1 There is..."
            2) "... was cited by Robert multiple times.1, 2, 3 There was also..."
        
        NOTE: this could lead to the creation of multiple dots in a sentence
        Example -> "We go outside.1 " turns into "We go outside.."

        Args:
            text_str (str): A string from which to remove reference numbers.

        Returns:
            str: The same string/sentence without reference numbers.
        """
        pattern = r'(\.|\?|\!|\‘|\’|\;|\:)(\d+(?:,\s*\d+)*,?)' # captured groups e.g. [.1], [.1,2,], [.1,2,3]
        return re.sub(pattern, '.', text_str)

    def remove_leading_commas(self, text_str: str) -> str:
        """
        Removes leading commas with empty space around them after a dot.

        This can occur when multiple reference numbers separated by commas 
        are removed from the text which leaves scattered commas that can 
        intefere with sentence splitting process. 
        
        E.g. ".1, 2,3 Here goes another sentence." -> ". ,  , Here goes another sentence."

        Args:
            text_str (str): Text string to remove leading commas from

        Returns:
            str: The text string without leading commas after a dot
        """
        return re.sub(r'\.(\s*,\s*)+', '. ', text_str)

    def remove_extra_periods(self, text_str: str) -> str:
        """
        This function removes dots/periods from a sentence/string as that is considered as noise.
        Removing  also helps decrease amount of tokens to pass to the model.

        NOTE: This function now prevents extra whitespaces after single dots of decimal digits.
                e.g. -> "1.19" now stays as is which is correct. 
                But this also leads to this "1. ... ." -> "1.."
                This can be resolved using rstrip on "." char to remove all the dots.

        NOTE: in some cases, after removal of multiple dots, the word that comes after is appended
              immediately after the sentence.
              example: "That is cool.. No, this is cooler." -> "This is cool.No, this is cooler."
              UPDATE: this issue is resolved. Whitespace is added after ending dots.

        Example sentences: 
            1) "This sentence is extracted with extra dots...."
            2) "... Was there when it happened"

        Args:
            text_str (str): A string from which to remove extra dots/periods.

        Returns:
            str: The same string/sentence without extra dots/periods.
        """
        # Replace sequences of dots (with or without spaces) with a single dot followed by a space
        # Replace multiple dots with a single dot and a space. 
        # cleaned_string = re.sub(r'\s*\.{1,}\s*', '.', text_str)
        # cleaned_string = re.sub(r'(?<!\d)\s*\.{2,}\s*(?!\d)', '.', text_str)
        cleaned_string = re.sub(r'(?<!\d)(?:\s*\.){2,}\s*(?!\d)', '. ', text_str)
        
        # Ensure multiple dots are replaced with a single dot
        # Add space after the dot to ensure right spacing between sentences
        # cleaned_string = re.sub(r'\.+', '. ', cleaned_string)
        # cleaned_string = re.sub(r'(?<!\d)\.+(?!\d)', '. ', cleaned_string)
        cleaned_string = re.sub(r'\s+\.', '.', cleaned_string)
        
        # Remove leading/trailing dots
        # cleaned_string = re.sub(r'^\.+|\.+$', '', cleaned_string)

        # Remove only leading to prevent remove trailing dot that is part of sentence!
        cleaned_string = re.sub(r'^\.+', '', cleaned_string)

         # Strip leading/trailing whitespace
        cleaned_string = cleaned_string.strip()

        return cleaned_string

    def pre_process_txt(
        self, 
        extracted_txt_str: List[str],
        remove_ref_numbers: bool = False,
        remove_punctuations: bool = False,
        remove_punctuations_at_end: bool = False,
        remove_extra_periods: bool = False
    ) -> List[str]:
        """
        Pre-processing text given a list of strings. 
        This function helps clean the sentences from possible noise after being extracted.
        
        Args:
            extracted_txt_str (List[str]): The texted extracted by a parser as a list

        Returns:
            List[str]: Pre-processed list of strings
        """
        for i, curr_str in enumerate(extracted_txt_str):
            # remove trailing whitespaces and extra whitespaces placed between words
            curr_str = curr_str.strip()

            # Remove the "-" from the last word and join it with first word in next senctence
            # in order to complete the word. When glued together, the second half is removed from next sentence.
            if curr_str.endswith('-'):
                # take into account that '-' can be in the last sentence.
                # in this case, remove it only.
                words = curr_str.split()
                if i+1 < len(extracted_txt_str):
                    first_half = words[-1].rstrip('-')
                    split_next_sentence = extracted_txt_str[i+1].split()
                    second_half = split_next_sentence[0]
                    words[-1] = first_half.strip() + second_half.strip()
                    extracted_txt_str[i+1] = " ".join(split_next_sentence[1:])
                else:
                    words[-1] = words[-1].rstrip('-')
                curr_str = " ".join(words)

            # Remove numbers or list of numbers directly after a period.
            # This in some books can occur when text is references.
            if remove_ref_numbers:
                curr_str = self.remove_ref_numbers(curr_str)

            # Sometimes multiple dots are recognized instead of one
            # for ending a sentence or for continuing a sentence. 
            # Remove extra dots since we only care about one.
            if remove_extra_periods:
                curr_str = self.remove_extra_periods(curr_str)

            # remove punctuations from sentences so that voice generations
            # is less likely to contain gibberish noise, repeating or unintelligible sound
            if remove_punctuations_at_end:
                curr_str = self.remove_punctuations_at_end(curr_str)
            
            if remove_punctuations:
                curr_str = self.remove_punctuations(curr_str) 

            self.logger.debug(f"{i}, pre-processed string: {curr_str}" )

            extracted_txt_str[i] = curr_str

        return extracted_txt_str