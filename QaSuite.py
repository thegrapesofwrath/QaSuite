#%%
import NotebookReport
import MarkdownLinkReport
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
@click.option('--kernel', default = 'python3', help='This is the kernel to use when parsing the notebook. Default: "python"')
@click.option('--overwrite', default = False, help='Enabling this will overwrite the notebook with the output of the report.')
def nbReport(directory,overwrite,kernel):
    '''Notebook Report.

    The Notebook Report will recurse a directory and check all .ipynb files using the nbconvert ExecutionPreprocessor. 
    It will save the output to the same file name and will list all failing notebooks as well as their cells that failed with the associated stack trace.
    '''
    NotebookReport.NotebookReport(directory=directory,overwrite=overwrite,kernel=kernel)

commandLineInterface.add_command(nbReport)

@click.command()
@click.option('--directory', default = './', help='The directory to run the link checker. It will recurse and check all markdown files in subdirectories.')
def mdLinkCheck(directory):
    '''Markdown Link Checker.

    This report will check all markdown links to see if they are valid on the file system 
    or if they return a valid status code from a get request. It will check both markdown
    links and html img tag links.
    '''
    MarkdownLinkReport.MarkdownLinkReport(directory=directory)

commandLineInterface.add_command(mdLinkCheck)

#%%
if __name__ == "__main__":
    commandLineInterface()