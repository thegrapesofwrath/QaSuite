'''Markdown Link Checker.

This report will check all markdown links to see if they are valid on the file system 
or if they return a valid status code from a get request. It will check both markdown
links and html img tag links.
'''
#%%
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
#%%
# testDirectory = "/Users/shartley/Documents/qaSuite/TestModules"
#%%
class MarkdownLinkReport():

    # def __init__(self,directory='./') -> None:
    def __init__(self,directory) -> None:
        self.markdownFiles: list = []
        self.rootDirectory = Path(directory)
        self.sucessfulLinks: list = {}
        self.failedLinks: list = {}
        self.parentDirectory = None
        self.markdownLinkMatch: object = re.compile(r'(?P<linkName>\[[\s\S]*\])(?P<link>\([\s\S]*\))')
        self.htmlLinkMatch: object = re.compile(r'(?P<link><img.+src="(.*)".*?>)')
        print("Starting Markdown Link Report:")
        self.populateMarkdownDocumentList()
        self.checkLinks()
        print(self.__repr__())
    
    def __repr__(self) -> str:
        report: str = ""
        totalSucessfulLinks: int = len(self.sucessfulLinks)
        totalFailedLinks: int = len(self.failedLinks)

        report += "\n\n===Sucesses===\n\n"
        for name,link in self.sucessfulLinks.items():
            report += f"{name} : {link}\n"
        report += "\n\n===FAILURES===\n\n"
        for name,link in self.failedLinks.items():
            report += f"{name} : {link}\n"
        report += "\n\n===SUMMARY===\n\n"
        report += f"Total Passing Links : {totalSucessfulLinks} \t Total Failing Links : {totalFailedLinks}"
        return report
        
    
    def populateMarkdownDocumentList(self) -> list:
        self.markdownFiles = list(self.rootDirectory.rglob("**/*.md"))

    def checkLinks(self) -> None:
        lineNumber: int = 0
        for file in self.markdownFiles:
            lineNumber = 0
            print('.')
            filePath: object = file.resolve()
            self.parentDirectory = file.parent

            try:
                _fileText: object = open(filePath,'r')
                fileText: list = _fileText.readlines()
                self.checkText(file,fileText,lineNumber)
                print("Markdown Link Report Finished.\n")
            except IsADirectoryError as e:
                _potentialFileName: list = file.name.split('.')
                potentialFileName: str = _potentialFileName[0]
                self.failedLinks[f"{file.parent}/{file.name}"] = f"Is a directory and not a file. Should it be named {potentialFileName}? Files in this directory have not been checked. Please rerun the report after fixing the issue."
                print(f"{file.name} a directory and not a file. Should it be named {potentialFileName}? Files in this directory have not been checked. Please rerun the report after fixing the issue.")
    
    def getLink(self,line: str, matchingRegex: object) -> str:
        link: object = matchingRegex.search(line)
        link: str = link.group('link')
        link: str = link[1:len(link)-1]
        return link

    def validateFileSystem(self,link: str) -> bool:
        linkPath: object = self.parentDirectory / link
        if linkPath.exists():
            return True
        elif self.validateURLRequest(link):
            return True
        else:
            return False
    
    def validateURLRequest(self,link: str) -> bool:
        try:
            request: object = requests.get(link)
            if request.status_code == 200:
                return True
            else:
                return False
        except Exception:
            pass
    
    def checkText(self,file: object, fileText: list, lineNumber: int) -> None:
        for line in fileText:    
            if self.markdownLinkMatch.search(line):
                link: str = self.getLink(line,self.markdownLinkMatch)
                if self.validateFileSystem(link):
                    self.sucessfulLinks[f"{file.name} - {lineNumber}"] = f"{link}"
                else:
                    self.failedLinks[f"{file.parent}/{file.name} - {lineNumber}"] = f"{link}"
            if self.htmlLinkMatch.match(line):
                link: str = self.getLink(line,self.htmlLinkMatch)
                tag: object = BeautifulSoup(f"<{link}>",'html.parser')
                imgTag: object = tag.find('img')
                srcLink: str = imgTag.get("src")
                if self.validateURLRequest(srcLink):
                    self.sucessfulLinks[f"{file.name} - {lineNumber}"] = f"{link}"
                else:
                    self.failedLinks[f"{file.parent}/{file.name} - {lineNumber}"] = f"{link}"
            lineNumber += 1



#%%
# markdownLinkReport = MarkdownLinkReport(testDirectory)
#%%