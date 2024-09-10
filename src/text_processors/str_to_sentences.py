# # -*- coding: utf-8 -*-
# import re
# alphabets= "([A-Za-z])"
# prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
# suffixes = "(Inc|Ltd|Jr|Sr|Co)"
# starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
# acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
# websites = "[.](com|net|org|io|gov|edu|me)"
# digits = "([0-9])"
# multiple_dots = r'\.{2,}'


# # def flatten_outer(nested_list):
# #     if isinstance(nested_list, list) and len(nested_list) == 1 and isinstance(nested_list[0], list):
# #         return nested_list[0]
# #     return nested_list

# def split_into_sentences(text: str) -> list[str]:
#     """
#     FROM https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences

#     Split the text into sentences.

#     If the text contains substrings "<prd>" or "<stop>", they would lead 
#     to incorrect splitting because they are used as markers for splitting.

#     :param text: text to be split into sentences
#     :type text: str

#     :return: list of sentences
#     :rtype: list[str]
#     """
#     text = " " + text + "  "
#     text = text.replace("\n"," ")
#     text = re.sub(prefixes,"\\1<prd>",text)
#     text = re.sub(websites,"<prd>\\1",text)
#     text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
#     text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
#     if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
#     text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
#     text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
#     text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
#     text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
#     text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
#     text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
#     text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
#     # TODO: handle edge case where sentences ending with a period followed immediately
#     # by an uppercase letter without a space in between (common in Dutch).
    
#     if "”" in text: text = text.replace(".”","”.")
#     if "\"" in text: text = text.replace(".\"","\".")
#     if "!" in text: text = text.replace("!\"","\"!")
#     if "?" in text: text = text.replace("?\"","\"?")
#     text = text.replace(".",".<stop>")
#     text = text.replace("?","?<stop>")
#     text = text.replace("!","!<stop>")
#     text = text.replace("<prd>",".")
#     sentences = text.split("<stop>")
#     sentences = [s.strip() for s in sentences]
#     if sentences and not sentences[-1]: sentences = sentences[:-1]
#     return sentences

import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

def split_into_sentences(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    
    # Handle single-letter sentence endings and preserve names with initials
    text = re.sub(r'\s([A-Z])\.(?=\s[A-Z][a-z])', r' \1<prd>', text)  # Preserve initials in names
    text = re.sub(r'\s([A-Z])\.(?=\s[A-Z][A-Z])', r' \1<prd>', text)  # Handle cases like "U. S. A."
    text = re.sub(r'\s([A-Z])\.(?=\s[^A-Z]|\s*$)', r' \1<prd><stop>', text)  # End sentence for single letter

    text = re.sub(r"\s([A-Za-z])[.]\s([A-Z])", r" \1<prd> <stop>\2", text)  # Split sentences where a sentence ends with a letter
    text = re.sub(r"\s([A-Za-z])[.]\s([a-z])", r" \1<prd> \2", text)  # Don't split sentences where a sentence ends with a letter followed by a lowercase letter

    text = re.sub("\s" + alphabets + "[.] (?=[a-zA-Z])"," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)

    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences