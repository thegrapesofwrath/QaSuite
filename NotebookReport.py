'''Notebook Report.

The Notebook Report will recurse a directory and check all .ipynb files using the nbconvert ExecutionPreprocessor. 
It will save the output to the same file name and will list all failing notebooks as well as their cells that failed with the associated stack trace.
'''
#%%
from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError
import subprocess
#%%
# testDirectory = "/Users/shartley/Documents/qaSuite/1-Recommended"

#%%
class NotebookReport():

    def __init__(self,directory, overwrite) -> None:
        self.notebooks: list = []
        self.overwrite = overwrite
        self.rootDirectory = Path(directory)
        self.sucessfulNotebooks: list = {}
        self.failedNotebooks: list = {}
        print("Starting Notebook Report:")
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
        for notebook in self.notebooks:
            print('.')
            notebookPath: object = notebook.resolve()

            _noteText: object = open(notebookPath,'r')
            noteText: str = _noteText.read()

            notebookParsed: object = nbformat.reads(noteText, as_version=4)

            executionPreprocessor: object = ExecutePreprocessor(timeout=600, kernel_name='python3',allow_errors=False)

            try:
                executionPreprocessor.preprocess(notebookParsed, {'metadata': {'path': str(notebook.parent)}})
                self.sucessfulNotebooks[str(notebook)] = 'PASS'
            except CellExecutionError as e:
                errorMessage = f'Error executing the notebook {str(notebook)}.\n\n'
                self.failedNotebooks[str(notebook)] = f"FAILED: {e} \n\n===\n\n"
                print(errorMessage)
            finally:
                if self.overwrite == True:
                    with open(str(notebook), mode='w', encoding='utf-8') as f:
                        nbformat.write(notebookParsed, f)
        print("Notebook Report Finished.\n")

#%%
# notebookReport = NotebookReport(testDirectory)
#%%
