"""Jupyter Notebook Spell Checker.

This module parses all notebooks and runs cspell on the code and
markdown cells. Any misspelled words are added to a set of words.
This set of words is printed at the very end. It is recommended to
run this code per unit and update the unit-level spelling dictionary.
"""
#%%
import subprocess
import nbformat
import progressbar
from pathlib import Path
# from ReportBase import ReportBase
from Reports.ReportBase import ReportBase
#%%
# testDirectory = "/Users/shartley/Documents/qaSuite/TestModules"
# testDirectory = "/Users/shartley/Documents/qaSuite/BadSpelling"
# testDirectory = "/Users/shartley/Documents/qaSuite/TestModules/BadSpelling"


#%%
class SpellCheckNotebookReport(ReportBase):

    # def __init__(self,directory='./',cSpellConfig = './cSpell.json') -> None:
    def __init__(self,directory,cspellconfig) -> None:
        super(SpellCheckNotebookReport, self).__init__(directory=directory)
        self.reportName = "Spellcheck Notebook"
        self.fileType = "ipynb"
        self.cSpellConfig = cspellconfig
        self.run()

    def runReport(self) -> None:
        self.cellNumber: int = 0
        i = 0
        bar = progressbar.ProgressBar(max_value=len(self.fileList))
        for file in self.fileList:
            self.cellNumber = 0
            noteText: str = self.readFile(file)
            notebookParsed: object = nbformat.reads(noteText, as_version=4)
            for cell in notebookParsed.cells:
                if cell.cell_type == 'markdown' or cell.cell_type == 'code':
                    spellingErrors = self.checkSpelling(cell)
                    if len(spellingErrors) > 0:
                        self.failedInstances[f"{file} - {self.cellNumber}"] = spellingErrors
                self.cellNumber += 1
            bar.update(i)
            i += 1
        print("Spellcheck Notebook Report Finished.\n")
    
    def checkSpelling(self,cell: object) -> list:
        self.writeTempFile(cell=cell)
        if cell.cell_type == 'code':
            executionObject: subprocess.CompletedProcess = self.runSubprocess(commandName='cspell',commandArgs=['--no-summary','--wordsOnly','--languageId','python','--config',self.cSpellConfig],fileName=self.tempFileName)
        else:
            executionObject: subprocess.CompletedProcess = self.runSubprocess(commandName='cspell',commandArgs=['--no-summary','--wordsOnly','--config',self.cSpellConfig],fileName=self.tempFileName)
        self.deleteTempFile()
        return self.cleanCspell(executionObject)

    def cleanCspell(self,executionObject: subprocess.CompletedProcess) -> list:
        spellingErrors: list = []
        stdOut: str = str(executionObject.stdout)
        outputList: list = stdOut.split('\\n')
        outputList[0] = outputList[0][1:]
        if len(outputList) > 1:
            for misspelling in outputList:
                misspelling = misspelling.strip("'\"")
                if len(misspelling) > 1:
                    spellingErrors.append(misspelling)
        return spellingErrors

#%%
# spellCheckNotebookReport = SpellCheckNotebookReport(testDirectory)
