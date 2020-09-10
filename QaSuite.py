#%%
import NotebookReport
import click

#%%
@click.group()
def commandLineInterface():
    '''QA Tools
    This is the QA Suite of Tools.

    It contains:

    Notebook Report       - Runs all jupyter notebooks and checks for errors.
    Markdown Link Checker - Checks that all markdown links are valid.
    '''
    pass

@click.command()
@click.option('--directory', default = './', help='The directory to run the notebook report. It will recurse and check all jupyter notebooks in subdirectories.')
@click.option('--overwrite', default = False, help='Enabling this will overwrite the notebook with the output of the report.')
def runNotebookReport(directory,overwrite):
    '''Notebook Report.

The Notebook Report will recurse a directory and check all .ipynb files using the nbconvert ExecutionPreprocessor. 
It will save the output to the same file name and will list all failing notebooks as well as their cells that failed with the associated stack trace.
    '''
    NotebookReport.NotebookReport(directory=directory,overwrite=overwrite)

commandLineInterface.add_command(runNotebookReport)

#%%
if __name__ == "__main__":
    commandLineInterface()