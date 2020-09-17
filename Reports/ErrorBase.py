'''Base Error Class

This is the base error class for capturing errors/stack traces etc.
'''
class ErrorBase():
    def __init__(self,isError: bool,fileObject: object = None,lineNumber: int = None, exceptionObject: object = None):
        self.isError = isError
        self.fileObject = fileObject
        self.lineNumber = lineNumber
        self.exceptionObject = exceptionObject
