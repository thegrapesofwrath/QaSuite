"""Jupyter Notebook Spell Checker.

This module parses all notebooks and runs cspell on the code and
markdown cells. Any misspelled words are added to a set of words.
This set of words is printed at the very end. It is recommended to
run this code per unit and update the unit-level spelling dictionary.
"""
#%%
import subprocess
import nbformat
from ReportBase import ReportBase
#%%
testDirectory = "/Users/shartley/Documents/qaSuite/TestModules"


#%%
class SpellCheckReport(ReportBase):

    def __init__(self,directory='./') -> None:
        super(SpellCheckReport, self).__init__(directory=directory)
        self.reportName = "Notebook Spell Check"
        self.fileType = "ipynb"
        self.run()

    def runReport(self) -> None:
        self.cellNumber: int = 0
        for file in self.fileList:
            self.cellNumber = 0
            print('.')

            noteText: str = self.readFile(file)

            notebookParsed: object = nbformat.reads(noteText, as_version=4)

            notebookResult: dict = {}

            for cell in notebookParsed.cells:
                if cell.cell_type == 'markdown' or cell.cell_type == 'code':
                    spellingErrors = self.checkSpelling(cell)
                    if spellingErrors != None:
                        notebookResult[f"{file} - {self.cellNumber}"] = spellingErrors
                
                self.cellNumber += 1


        print("Spellcheck Report Finished.\n")
    
    def checkSpelling(self,cell) -> list:
        if cell.cell_type == 'code':
            self.writeTempFile(self.tempFileName)
            executionObject: subprocess.CompletedProcess = self.runSubprocess(commandName='cspell',commandArgs=['--no-summary'],fileName=self.tempFileName)
            self.deleteTempFile(self.tempFileName)
            return self.cleanCspell(executionObject)
        else:
            None
    

    def cleanCspell(self,executionObject: subprocess.CompletedProcess) -> list:
        stdOut: str = executionObject.stdout
        outputList: list = stdOut.split('\\n')
        outputList[0] = outputList[0][1:]
        outputList = outputList[1:len(outputList) - 1]
        return outputList

#%%
spellCheckReport = SpellCheckReport(testDirectory)
