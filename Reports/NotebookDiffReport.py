'''Notebook Diff Report.


'''
#%%
from pathlib import Path
import tokenize
import subprocess
# import nbformat
# import progressbar
# from nbconvert.preprocessors import ExecutePreprocessor
# from nbconvert.preprocessors import CellExecutionError
# import os

# from ReportBase import ReportBase
from Reports.ReportBase import ReportBase
#%%
# testDirectory = "/Users/shartley/Documents/qaSuite/TestModules/Activities/05-Stu_Columns/"
testDirectory = "/Users/shartley/Documents/qaSuite/TestModules/"

#%%
class NotebookDiffReport(ReportBase):

    def __init__(self,directory,writeLog,logFileName) -> None:
        super(NotebookDiffReport, self).__init__(directory=directory,writeLog=writeLog,logFileName=logFileName)
        self.kernel = 'python3'
        self.reportName = "Notebook Diff"
        self.fileType = "ipynb"
        self.activityPairs = {}
        self.run()

    def runReport(self) -> None:
        self.populateActivityPairs()
        self.checkForMissingActivities()
        self.gitDiffFiles()
        # print(self.activityPairs)
        for activity in self.activityPairs:
            for solvedActivity in activity["Solved"]:
                self.countSubProcess()
                unsolvedActivity = activity["Unsolved"][activity["Unsolved"].index(solvedActivity)]

                notebookSolvedParsed = self.parseNotebook(file=solvedActivity)
                notebookUnsolvedParsed = self.parseNotebook(file=unsolvedActivity)
                self.cellNumber = 0
                if notebookSolvedParsed != None and notebookUnsolvedParsed != None:
                    for solvedCell in notebookSolvedParsed.cells:
                        self.countSubProcess()
                        
                        if solvedCell.cell_type == 'code':
                            unSolvedCell = notebookSolvedParsed.cells[self.cellNumber]
                            if self.checkCellGreaterThan(solvedCell,unSolvedCell):
                                self.sucessfulInstances[f"{solvedActivity} - Cell:{self.cellNumber}"] = 'PASSED'
                            else:
                                self.failedInstances[f"{solvedActivity} - Cell:{self.cellNumber}"] = 'FAILED'
                        
                        if solvedCell.output_type == 'display_data' or solvedCell.output_type == 'execute_result':
                            unSolvedCell = notebookSolvedParsed.cells[self.cellNumber]
                            if self.checkCellEquality(solvedCell,unSolvedCell):
                                self.sucessfulInstances[f"{solvedActivity} - Cell:{self.cellNumber}"] = 'PASSED'
                            else:
                                self.failedInstances[f"{solvedActivity} - Cell:{self.cellNumber}"] = 'FAILED'
                        
                        self.cellNumber += 1
                else:
                    print("A notebook was unable to be parsed. It is not in valid json format or it is empty.")
                    self.countProcessComplete()
                self.countProcessComplete()
        print("\nNotebook Diff Report Finished.\n")
    
    def populateActivityPairs(self) -> None:
        ''' Populate the a dictionary of the Solved and Unsolved activities sets. '''
        for file in self.fileList:
            self.countSubProcess()
            if file.parents[1] not in self.activityPairs and file.parents[2].name == 'Activities':
                self.activityPairs[file.parents[1]] = {"Solved" : [], "Unsolved" : []}
            if file.parents[0].name == "Solved":
                self.activityPairs[file.parents[1]]["Solved"].append(file)
            elif file.parents[0].name == "Unsolved":
                self.activityPairs[file.parents[1]]["Unsolved"].append(file)
    
    def checkForMissingActivities(self) -> None:
        '''Check for missing activities between solved and unsolved folders. Will throw an error if Solved and Unsolved folder lengths are different.'''
        self.countSubProcess()
        pass

    def checkCellEquality(self,cell1: object, cell2: object) -> bool:
        ''' Check if two cell objects are equal. cell1 == cell2 '''
        self.countSubProcess()
        if cell1 == cell2:
            return True
        else:
            return False
    
    def checkCellGreaterThan(self,cell1:object,cell2:object) -> bool:
        ''' Check if the content of cell1 is greater than cell2. cell1 >= cell2 '''
        self.countSubProcess()
        tokenizeCell1 = self.tokenizeCell(cell1)
        tokenizeCell2 = self.tokenizeCell(cell2)
        if tokenizeCell1 >= tokenizeCell2:
            return True
        else:
            return False

    
    def tokenizeCell(self,cell: object) -> tuple:
        ''' Tokenize the python cell and remove all comments and docstrings. '''
        self.countSubProcess()
        pass

    def gitDiffFiles(self) -> None:
        executionObject: subprocess.CompletedProcess = self.runSubprocess(commandName='git',commandArgs=['diff','--diff-filter=d','master'],fileName=None)
        # return executionObject
        pass



#%%
notebookDiffReport = NotebookDiffReport(testDirectory,writeLog=False,logFileName=None)
#%%
