'''Report Base.

This is the base report class that reports will inherit from.
'''
#%%
from pathlib import Path
import subprocess
import requests
import os
import sys
import nbformat
import json

# from ErrorBase import ErrorBase
from Reports.ErrorBase import ErrorBase


#%%
class ReportBase(object):

    def __init__(self,directory,writeLog,logFileName) -> None:
        self.fileList: list = []
        self.reportName = ""
        self.fileType = ""
        self.rootDirectory = Path(directory)
        self.sucessfulInstances: dict = {}
        self.failedInstances: dict = {}
        self.reportOperationErrors: list = []
        self.lineNumber = 0
        self.cellNumber = 0
        self.tempFileName = 'deleteme'
        self.writeLog = writeLog
        self.logFileName = logFileName
    
    def __repr__(self) -> str:
        report: str = ""
        totalSucessfulInstances: int = len(self.sucessfulInstances)
        totalFailedInstances: int = len(self.failedInstances)
        totalOperationalErrors: int = len(self.reportOperationErrors)

        report += "\n\n===Sucesses===\n\n"
        for instance,status in self.sucessfulInstances.items():
            report += f"{instance} : {status}\n"
        report += "\n\n===FAILURES===\n\n"
        for instance,status in self.failedInstances.items():
            report += f"{instance} : {status}\n"
        report += "\n\n===OPERATIONAL ERRORS===\n\n"
        for error in self.reportOperationErrors:
            for instance,status in error:
                report += f"{instance} : {status}\n"
        report += "\n\n===SUMMARY===\n\n"
        report += f"Total Passing Instances : {totalSucessfulInstances} \t Total Failing Instances : {totalFailedInstances} \t Total Operational Errors : {totalOperationalErrors}"
        return report
        
    
    def populateFileList(self) -> list:
        try:
            if self.rootDirectory.exists():
                self.fileList = list(self.rootDirectory.rglob(f"**/*.{self.fileType}"))
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print(f"The directory: {self.rootDirectory} does not exist.")
            sys.exit(1)
    
    def run(self):
        print(f"Starting {self.reportName} Report:")
        self.populateFileList()
        self.runReport()
        if self.writeLog:
            self.writeLogFile()
        print(self.__repr__())
    
    def runReport(self):
        pass
    
    def writeTempFile(self,fileName: str = None,cell: object = None, preProcessingCommands: str = None) -> None:
        if fileName == None:
            fileName = self.tempFileName
        try:
            tempFile = open(file=fileName, mode="w")
            if preProcessingCommands != None:
                tempFile.write(preProcessingCommands)
            tempFile.write(cell.source)
            tempFile.close()
        except Exception as e:
            self.reportOperationErrors.append(ErrorBase(isError=True,fileObject = Path(fileName),exceptionObject= e))
    
    def deleteTempFile(self, fileName: str = None) -> None:
        if fileName == None:
            fileName = self.tempFileName
        try:
            os.remove(fileName)
        except Exception as e:
            self.reportOperationErrors.append(ErrorBase(isError=True,fileObject = Path(fileName),exceptionObject= e))

    def runSubprocess(self,commandName: str, commandArgs: list, fileName: str) -> subprocess.CompletedProcess:
        commandToRun = [commandName] + commandArgs + [fileName]
        completedProcess: subprocess.CompletedProcess = subprocess.run(
            commandToRun, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return completedProcess
    
    def readFile(self,file: Path, returnList: bool = False):
        filePath: object = file.resolve()
        self.parentDirectory = file.parent
        try:
            _fileText: object = open(filePath,'r')
            if returnList:
                fileText: list = _fileText.readlines()
            else:    
                fileText: str = _fileText.read()
            return fileText
        except IsADirectoryError:
            _potentialFileName: list = file.name.split('.')
            potentialFileName: str = _potentialFileName[0]
            self.failedInstances[f"{file.parent}/{file.name}"] = f"Is a directory and not a file. Should it be named {potentialFileName}? Files in this directory have not been checked. Please rerun the report after fixing the issue."
            print(f"{file.name} a directory and not a file. Should it be named {potentialFileName}? Files in this directory have not been checked. Please rerun the report after fixing the issue.")
    
    def validateFileSystem(self,link: str, tryValidateHTTP: bool = False) -> bool:
        linkPath: Path = self.parentDirectory / link
        if linkPath.exists():
            return True
        elif tryValidateHTTP and self.validateURLRequest(link):
            return True
        else:
            return False
    
    def validateURLRequest(self,link: str) -> bool:
        try:
            request: requests.Response = requests.get(link)
            if request.status_code == 200:
                return True
            else:
                return False
        except Exception:
            pass
    
    def checkForError(self, potentialError: ErrorBase):
        if potentialError.isError:
            self.reportOperationErrors.append(potentialError)
    
    def parseNotebook(self,file: Path) -> nbformat.NotebookNode:
        try:
            noteText: str = self.readFile(file)
            json.loads(noteText)
            parsedNotebook = nbformat.reads(noteText, as_version=4)
            return parsedNotebook
        except nbformat.ValidationError as e:
            print(f"{file} is not a valid ipynb file. Is it empty?\n{e}")
            self.failedInstances[f"{file.parent}/{file.name}"] = f"{file} is not a valid ipynb file. Is it empty?\n{e}\n{noteText}"
        except AttributeError as e:
            print(f"{file} is not a valid ipynb file. Is it empty?\n{e}")
            self.failedInstances[f"{file.parent}/{file.name}"] = f"{file} is not a valid ipynb file. Is it empty?\n{e}\n{noteText}"
        except Exception as e:
            print(f"{file} is not a valid ipynb file. Is it empty?\n{e}")
            self.failedInstances[f"{file.parent}/{file.name}"] = f"{file} is not a valid ipynb file. Is it empty?\n{e}\n{noteText}"
    
    def writeLogFile(self) -> None:
        if self.logFileName == None:
            logName: str = self.reportName.replace(' ','')
            fileName = f'{logName}.log'
        logFile = open(file=fileName,mode='w')
        logFile.write(self.__repr__())
        logFile.close()

# %%
