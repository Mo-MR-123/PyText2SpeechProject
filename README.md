# PyText2SpeechProject
Python project for implementing txt2speech from website, pdf or txt files. Motive: I don't like reading, I like listening :)

NOTE: This project is still ongoing. Use at your own risk!

## INFO TOOLS:  

Python version: 3.11.9  

## SETUP/INSTALATION STEPS DEV ENV:    

### Create environment using python-venv (make sure to have python-venv):
```
python -m venv venv
```

NOTE: try python3 if python points to another python version for some reason, to use python3.

### Navigate into the created venv folder and activate environment:
Linux:  
```
source venv/bin/activate
```

Windows:
```
source venv/Scripts/activate
```

### Install dependencies for the environment using the following script:
```
chmod +x install_env.sh
./install_env.sh
```

## PLAN:  
**1:** Find a good txt2speech model with a voice that is as natural and soothing as possible to listen to.  
**2:** Look out for tools to extract txt from pdf files. Add option to pass page range from which to extract txt. Keep footer and header info of pdf page in mind as that would lead to extraction of page numbers and other irrelevant txt in a page (is this even problematic? if so, how can we solve it? Brainstormed ideas: use regex to discard them, add option to remove header/footer txt if possible, this is all I have for now!!! )  
**3:** Structure of code has to be modular for readability and ease of change/modifications to the code. Use OOP. 
**4:** Add args parser for user to give params to the program.

## TODOS:  
- [x]  
from TTS, the "self.synthesizer.tts(...)" does not support list of text being passed since it is always assumed that input is string. This prohibits any way of using
own method for splitting sentences. To fix this change 
```
sens = [text]
```
to
```
if isinstance(text, list):
    sens = text
elif isinstance(text, str):
    sens = [text]
else: 
    sens = None
```

- [x] Changed to PyMuPDF as it is the most adequate pdf handler so far offering customizability.

- [x] For now, use of pymupdf to remove reference links embedded in pdf file works. More tests needed to verify with 100% certainty.

## GENERAL NOTES:

- Important link for going from XTTS v2.0.3 to v2.0.2 as that results in better synthesis according to most people: https://github.com/oobabooga/text-generation-webui/issues/4723

- Link for things to keep in mind when working with XTTS model to make sure cleaner output is realized: https://www.reddit.com/r/Oobabooga/comments/1807tsl/comment/ka5l8w9/?share_id=_5hh4KJTXrEOSP0hR0hCK&utm_content=2&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=1