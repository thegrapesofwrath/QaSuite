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

# from ReportBase import ReportBase
from Reports.ReportBase import ReportBase
#%%
# testDirectory = "/Users/shartley/Documents/qaSuite/TestModules"

#%%
class NotebookReport(ReportBase):

    def __init__(self,directory, overwrite) -> None:
        super(NotebookReport, self).__init__(directory=directory)
        self.overwrite = overwrite
        self.kernel = 'python3'
        self.reportName = "Notebook Report"
        self.fileType = "ipynb"
        self.run()

    def runReport(self) -> None:
        i = 0
        bar = progressbar.ProgressBar(max_value=len(self.fileList))
        for file in self.fileList:
            noteText: str = self.readFile(file)
            notebookParsed: object = nbformat.reads(noteText, as_version=4)
            executionPreprocessor: object = ExecutePreprocessor(timeout=600, kernel_name=self.kernel,allow_errors=False)
            try:
                executionPreprocessor.preprocess(notebookParsed, {'metadata': {'path': str(file.parent)}})
                self.sucessfulInstances[str(file)] = 'PASS'
            except CellExecutionError as e:
                errorMessage = f'Error executing the notebook {str(file)}.\n\n'
                self.failedInstances[str(file)] = f"FAILED: {e} \n\n===\n\n"
                print(errorMessage)
            finally:
                if self.overwrite == True:
                    with open(str(file), mode='w', encoding='utf-8') as f:
                        nbformat.write(notebookParsed, f)
            bar.update(i)
            i += 1
        print("Notebook Report Finished.\n")

#%%
# notebookReport = NotebookReport(testDirectory,overwrite=False)
#%%
