'''Report Base.

This is the base report class that reports will inherit from.
'''
#%%
from pathlib import Path
import subprocess
import requests

# from ErrorBase import ErrorBase


#%%
class ReportBase(object):

    def __init__(self,directory) -> None:
        self.fileList: list = []
        self.reportName = ""
        self.fileType = ""
        self.rootDirectory = Path(directory)
        self.sucessfulInstances: dict = {}
        self.failedInstances: dict = {}
        self.lineNumber = 0
        self.cellNumber = 0
        self.tempFileName = 'deleteme'

    
    def __repr__(self) -> str:
        report: str = ""
        totalSucessfulInstances: int = len(self.sucessfulInstances)
        totalFailedInstances: int = len(self.failedInstances)

        report += "\n\n===Sucesses===\n\n"
        for instance,status in self.sucessfulInstances.items():
            report += f"{instance} : {status}\n"
        report += "\n\n===FAILURES===\n\n"
        for instance,status in self.failedInstances.items():
            report += f"{instance} : {status}\n"
        report += "\n\n===SUMMARY===\n\n"
        report += f"Total Passing Instances : {totalSucessfulInstances} \t Total Failing Instances : {totalFailedInstances}"
        return report
        
    
    def populateFileList(self) -> list:
        self.fileList = list(self.rootDirectory.rglob(f"**/*.{self.fileType}"))
    
    def run(self):
        print(f"Starting {self.reportName} Report:")
        self.populateFileList()
        self.runReport()
        print(self.__repr__())
    
    def runReport(self):
        pass

    def writeTempFile(self,fileType: str) -> str:
        pass

    def deleteTempFile(self,fileName: str) -> bool:
        pass

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
        except IsADirectoryError as e:
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

# %%
