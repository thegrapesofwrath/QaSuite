"""Jupyter Notebook Spell Checker.

This module parses all notebooks and runs cspell on the code and
markdown cells. Any misspelled words are added to a set of words.
This set of words is printed at the very end. It is recommended to
run this code per unit and update the unit-level spelling dictionary.
"""
#%%
from pathlib import Path
import nbformat
# from nbconvert.preprocessors import ExecutePreprocessor
# from nbconvert.preprocessors import CellExecutionError
#%%
testDirectory = "/Users/shartley/Documents/qaSuite/TestModules"

#%%
class SpellCheckReport():

    def __init__(self,directory='./') -> None:
        self.notebooks: list = []
        self.rootDirectory = Path(directory)
        self.sucessfulCells: list = {}
        self.failedCells: list = {}
        print("Starting Spellcheck Report:")
        self.populateNotebooksList()
        self.checkNoteBooks()
        print(self.__repr__())
    
    def __repr__(self) -> str:
        report: str = ""
        totalSucessfulNotebooks: int = len(self.sucessfulNotebooks)
        totalFailedNotebooks: int = len(self.failedNotebooks)

        report += "\n\n===Sucesses===\n\n"
        for notebook,status in self.sucessfulNotebooks.items():
            report += f"{notebook} : {status}\n"
        report += "\n\n===FAILURES===\n\n"
        for notebook,status in self.failedNotebooks.items():
            report += f"{notebook} : {status}\n"
        report += "\n\n===SUMMARY===\n\n"
        report += f"Total Passing Notebooks : {totalSucessfulNotebooks} \t Total Failing Notebooks : {totalFailedNotebooks}"
        return report
        
    
    def populateNotebooksList(self) -> list:
        self.notebooks = list(self.rootDirectory.rglob("**/*.ipynb"))

    def checkNoteBooks(self) -> None:
        cellNumber: int = 0
        for notebook in self.notebooks:
            cellNumber = 0
            print('.')
            notebookPath: object = notebook.resolve()

            _noteText: object = open(notebookPath,'r')
            noteText: str = _noteText.read()

            notebookParsed: object = nbformat.reads(noteText, as_version=4)

            notebookResult: dict = {}

            for cell in notebookParsed.cells:
                if cell.cell_type == 'markdown' or cell.cell_type == 'code':
                    spellingErrors = self.checkSpelling(cell)
                    if spellingErrors != None:
                        notebookResult[f"{notebookPath}/{notebook.name} - {cellNumber}"] = spellingErrors
                
                cellNumber += 1


        print("Spellcheck Report Finished.\n")
    
    def checkSpelling(self,cell) -> list:
        if cell.cell_type == 'code':
            self.writeTempFile('deleteme.py')
            executionObject: object = self.runSubprocess('cspell',['check','./deleteme.py'])
            
        else:
            pass
    
    def writeTempFile(self,fileType: str) -> str:
        pass

    def deleteTempFile(self,fileName: str) -> bool:
        pass

    def runSubprocess(self,commandName: str, commandArgs: list, fileName: str) -> object:
        pass

    def cleanCspell(self,outputList: list) -> list:
        pass

#%%
spellCheckReport = SpellCheckReport(testDirectory)
#%%
# -*- coding: utf-8 -*-

# import re
# # import click
# import nbformat
# import subprocess
# from pathlib import Path
# from colorama import init, Fore, Style

# # Initialize Colorama (Windows Only)
# init()

# # Regex to highlight spelling issues
# cspell_regex = re.compile(r"(Unknown word: )(?P<word>.*?)\n", re.S)

# # Store all unknown words
# cspell_set = set()


# def check_code(linter_commands):
#     """Lint Notebook Code Cells."""
#     # Execute the linter
#     try:
#         completed = subprocess.run(
#             linter_commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
#         )
#     except subprocess.CalledProcessError as err:
#         print("Error: ", err)
#     else:
#         # Find any misspelled words and add to the set
#         matches = cspell_regex.search(completed.stdout.decode("utf-8"))
#         if matches:
#             cspell_set.add(matches.group("word"))


# def cli(notebook_directory):

#     # Create Paths
#     notebook_path = Path(notebook_directory)
#     # Find all notebooks
#     # Exclude notebooks ending in `-checkpoints`
#     notebooks = notebook_path.glob("**/*[!-checkpoints].ipynb")

#     for notebook_path in notebooks:

#         # Open each notebook and parse the code cells
#         with open(notebook_path, "r") as notebook:
#             nb = nbformat.read(notebook, as_version=4)
#             code_cells = [i.source for i in nb.cells if i.cell_type == "code"]
#             code_cells_str = "\n".join(code_cells).strip()
#             md_cells = [i.source for i in nb.cells if i.cell_type == "markdown"]
#             md_cells_str = "\n".join(md_cells).strip()

#             # Output the code cells to a temp file for linting
#             tmp_path = Path(f"deleteme")
#             tmp_path.write_text(code_cells_str)

#             print(f"Linting file: {notebook_path.resolve()}")

#             # Run cspell for code cells
#             linter_commands = ["cspell", "-u", tmp_path]
#             check_code(linter_commands)

#             # Output the markdown cells to a temp file for linting
#             tmp_path.write_text(md_cells_str)

#             # Run cspell for markdown cells
#             linter_commands = ["cspell", "-u", tmp_path]
#             check_code(linter_commands)

#             # Clean up temp file
#             tmp_path.unlink()

#     # Show the final set of misspelled words
#     print(cspell_set)
