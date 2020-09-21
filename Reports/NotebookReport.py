'''Notebook Report.

The Notebook Report will recurse a directory and check all .ipynb files using the nbconvert ExecutionPreprocessor. 
It will save the output to the same file name and will list all failing notebooks as well as their cells that failed with the associated stack trace.
'''
#%%
# from pathlib import Path
import nbformat
import progressbar
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError
import os

# from ReportBase import ReportBase
from Reports.ReportBase import ReportBase
#%%
# testDirectory = "/Users/shartley/Documents/qaSuite/TestModules"

#%%
class NotebookReport(ReportBase):

    def __init__(self,directory,writeLog,logFileName,overwrite,pauseForENV) -> None:
        super(NotebookReport, self).__init__(directory=directory,writeLog=writeLog,logFileName=logFileName)
        self.overwrite = overwrite
        self.kernel = 'python3'
        self.reportName = "Notebook"
        self.fileType = "ipynb"
        self.pauseForENV = pauseForENV
        self.run()

    def runReport(self) -> None:
        for file in self.fileList:
            notebookParsed: object = self.parseNotebook(file=file)
            executionPreprocessor: object = ExecutePreprocessor(timeout=600, kernel_name=self.kernel,allow_errors=False)
            try:
                executionPreprocessor.preprocess(notebookParsed, {'metadata': {'path': str(file.parent)}})
                self.sucessfulInstances[str(file)] = 'PASS'
            except CellExecutionError as e:
                errorMessage = f'\nError executing the notebook {str(file)} in one of the cells.\n\n'
                if e.ename == 'ValueError':
                    print(f"\nThe following value was not found: {e}")
                    progressbar.streams.flush()
                    if self.pauseForENV:
                        userCreatedVariable = self.createEnvironmentVariable()
                        if userCreatedVariable:
                            try:
                                executionPreprocessor.preprocess(notebookParsed, {'metadata': {'path': str(file.parent)}})
                                self.sucessfulInstances[str(file)] = 'PASS'
                            except Exception as e:
                                print(f"The notebook was still unsucessful: {e}")
                                self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                        else:
                            self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                    else:
                        self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                else:
                    self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                print(errorMessage)
            except AttributeError as e:
                errorMessage = f'\nError executing the notebook {str(file)}. It is possibly not valid json.\n\n'
                self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                print(errorMessage)
            except ValueError as e:
                print(f"The following value was not found: {e}")
                if self.pauseForENV:
                    userCreatedVariable = self.createEnvironmentVariable()
                    if userCreatedVariable:
                        try:
                            executionPreprocessor.preprocess(notebookParsed, {'metadata': {'path': str(file.parent)}})
                            self.sucessfulInstances[str(file)] = 'PASS'
                        except Exception as e:
                            print(f"The notebook was still unsucessful: {e}")
                            self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                    else:
                        self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                else:
                    self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
            except Exception as e:
                errorMessage = f'\nError executing the notebook {str(file)}.\n\n'
                self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                print(errorMessage)
            finally:
                self.countProcessComplete()
                if self.overwrite == True:
                    with open(str(file), mode='w', encoding='utf-8') as f:
                        nbformat.write(notebookParsed, f)
        print("\nNotebook Report Finished.\n")
    
    def createEnvironmentVariable(self) -> bool:
        print('\nWould you like to create an environment variable for the value?\n')
        progressbar.streams.flush()
        userInput: str = input("\nEnter (y/n):\n")
        if userInput == 'y':
            print("\nPlease enter the new variable name.\n")
            progressbar.streams.flush()
            newVariableName: str = input()
            print("\nPlease enter the variable's value.\n")
            progressbar.streams.flush()
            newVariableValue: str = input()
            os.environ[newVariableName] = str(newVariableValue)
            return True
        else:
            return False

#%%
# notebookReport = NotebookReport(testDirectory,overwrite=False)
#%%
