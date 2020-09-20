"""Jupyter Notebook Spell Checker.

This module parses all notebooks and runs cspell on the code and
markdown cells. Any misspelled words are added to a set of words.
This set of words is printed at the very end. It is recommended to
run this code per unit and update the unit-level spelling dictionary.
"""
#%%
import subprocess
import nbformat
from nbformat.reader import NotJSONError
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
    def __init__(self,directory,writeLog,logFileName,cSpellConfig) -> None:
        super(SpellCheckNotebookReport, self).__init__(directory=directory,writeLog=writeLog,logFileName=logFileName)
        self.reportName = "Spellcheck Notebook"
        self.fileType = "ipynb"
        self.cSpellConfig = cSpellConfig
        self.run()

    def runReport(self) -> None:
        self.cellNumber: int = 0
        fileCount: int = 0
        processCount = [0,0,len(self.fileList)]
        markers = [
        '\x1b[32m█\x1b[39m',  # Done
        '\x1b[33m#\x1b[39m',  # Processing
        '\x1b[31m.\x1b[39m',  # ToDo
    ]
        for file in self.fileList:
            widgets = [f'\x1b[33mProcessing ({processCount[0]}/{processCount[2]} files): {file.name}\x1b[39m',progressbar.MultiRangeBar(name='processCount',markers=markers)]
            cellProcessBar: progressbar.ProgressBar = progressbar.ProgressBar(widgets=widgets, max_value=len(self.fileList),redirect_stdout=True).start()
            self.cellNumber = 0
            notebookParsed: object = self.parseNotebook(file=file)
            if notebookParsed != None:
                for cell in notebookParsed.cells:
                    if cell.cell_type == 'markdown' or cell.cell_type == 'code':
                        spellingErrors = self.checkSpelling(cell)
                        if len(spellingErrors) > 0:
                            self.failedInstances[f"{file} - Cell:{self.cellNumber}"] = spellingErrors
                        else:
                            self.sucessfulInstances[f"{file} - Cell:{self.cellNumber}"] = 'PASSED'
                    self.cellNumber += 1
                    processCount[1] = self.cellNumber
                    cellProcessBar.update(processCount=processCount,force=True)
            else:
                print("The notebook was unable to be parsed. It is not in valid json format or it is empty.")
            fileCount += 1
            processCount[0] = fileCount
            cellProcessBar.update(processCount=processCount,force=True)
        cellProcessBar.finish()
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
