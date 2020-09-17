'''Markdown Link Checker.

This report will check all markdown links to see if they are valid on the file system 
or if they return a valid status code from a get request. It will check both markdown
links and html img tag links.
'''
#%%
import re
from bs4 import BeautifulSoup
import progressbar
# from ReportBase import ReportBase
# from ErrorBase import ErrorBase

from Reports.ReportBase import ReportBase
from Reports.ErrorBase import ErrorBase
#%%
# testDirectory = "/Users/shartley/Documents/qaSuite/TestModules"
#%%
class MarkdownLinkReport(ReportBase):

    # def __init__(self,directory='./') -> None:
    def __init__(self,directory) -> None:
        super(MarkdownLinkReport, self).__init__(directory=directory)
        self.markdownLinkMatch: object = re.compile(r'(?P<linkName>\[[\s\S]*\])(?P<link>\([\s\S]*\))')
        self.htmlLinkMatch: object = re.compile(r'(?P<link><img.+src="(.*)".*?>)')
        self.reportName = "Markdown Link Check"
        self.fileType = "md"
        self.run()

    def runReport(self) -> None:
        self.lineNumber: int = 0
        bar = progressbar.ProgressBar(max_value=len(self.fileList))
        i = 0
        for file in self.fileList:
            self.lineNumber = 0
            fileText: list = self.readFile(file,returnList=True)
            results: ErrorBase = self.checkText(file,fileText,self.lineNumber)
            if results.isError:
                print(f"Markdown Link Reporter failed for {results.fileObject} at {results.lineNumber}: {results.exceptionObject}")
            bar.update(i)
            i += 1
        print("Markdown Link Check Finished.\n")

    def getLink(self,line: str, matchingRegex: object) -> str:
        link: object = matchingRegex.search(line)
        link: str = link.group('link')
        link: str = link[1:len(link)-1]
        return link
    
    def checkText(self,file: object, fileText: list, lineNumber: int) -> ErrorBase:
        try:
            for line in fileText:    
                if self.markdownLinkMatch.search(line):
                    link: str = self.getLink(line,self.markdownLinkMatch)
                    if self.validateFileSystem(link,tryValidateHTTP=True):
                        self.sucessfulInstances[f"{file.name} - {self.lineNumber}"] = f"{link}"
                    else:
                        self.failedInstances[f"{file.parent}/{file.name} - {self.lineNumber}"] = f"{link}"
                if self.htmlLinkMatch.match(line):
                    link: str = self.getLink(line,self.htmlLinkMatch)
                    tag: object = BeautifulSoup(f"<{link}>",'html.parser')
                    imgTag: object = tag.find('img')
                    srcLink: str = imgTag.get("src")
                    if self.validateURLRequest(srcLink):
                        self.sucessfulInstances[f"{file.name} - {self.lineNumber}"] = f"{link}"
                    else:
                        self.failedInstances[f"{file.parent}/{file.name} - {self.lineNumber}"] = f"{link}"
                self.lineNumber += 1
            return ErrorBase(isError=False,fileObject=file,lineNumber=self.lineNumber,exceptionObject=None)
        except Exception as e:
            return ErrorBase(isError=True,fileObject=file,lineNumber=self.lineNumber,exceptionObject=e)

#%%
# markdownLinkReport = MarkdownLinkReport(testDirectory)
# %%
