# PyText2SpeechProject
Python project for implementing txt2speech from website, pdf or txt files. Motive: I don't like reading, I like listening :)

NOTE: This project is still ongoing. Use at your own risk!

## INFO TOOLS:  

Python version: 3.12.0  

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

### Install dependencies using pip (package manager for python):
```
pip install -r requirements.txt
```

## PLAN:  
**1:** Find a good txt2speech model with a voice that is as natural and soothing as possible to listen to.  
**2:** Look out for tools to extract txt from pdf files. Add option to pass page range from which to extract txt. Keep footer and header info of pdf page in mind as that would lead to extraction of page numbers and other irrelevant txt in a page (is this even problematic? if so, how can we solve it? Brainstormed ideas: use regex to discard them, add option to remove header/footer txt if possible, this is all I have for now!!! )  
**3:** Structure of code has to be modular for readability and ease of change/modifications to the code. Use OOP. 
**4:** Add args parser for user to give params to the program.
