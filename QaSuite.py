#%%
from Reports.NotebookReport import NotebookReport
from Reports.MarkdownLinkReport import MarkdownLinkReport
from Reports.SpellCheckNotebookReport import SpellCheckNotebookReport
import click

#%%
@click.group()
def commandLineInterface():
    '''QA Tools
    This is the QA Suite of Tools.

    It contains:

    Notebook Report       - Runs all jupyter notebooks and checks for errors.
    Markdown Link Checker - Checks that all markdown links are valid.
    Notebook Spell Checker - Checks the spelling in all markdown and code cells for a jupyter notebook.
    '''
    pass

@click.command()
@click.option('--directory',type = str,required = False, default = './',show_default = True, help='The directory to run the notebook report. It will recurse and check all jupyter notebooks in subdirectories.')
@click.option('--writeLog', type = bool, required = False ,default = False,show_default = True, help='This will write the output to a log file. The default value is "False".')
@click.option('--logFileName', type = str, required = False,default = None,show_default = True, help='Use this to change the default name of the log file. The default value is <report_name>.log')
@click.option('--overwrite', type = bool,required = False,default = False,show_default = True, help='Enabling this will overwrite the notebook with the output of the report.')
@click.option('--pauseForENV', type = bool,required = False,default = False,show_default = True, help='Enabling this will pause execution is a missing environment variable is found. The user will have a chance to enter the variable and rerun the report.')
def nbReport(directory,writelog,logfilename,overwrite,pauseforenv):
    '''Notebook Report.

    The Notebook Report will recurse a directory and check all .ipynb files using the nbconvert ExecutionPreprocessor. 
    It will save the output to the same file name and will list all failing notebooks as well as their cells that failed with the associated stack trace.
    '''
    NotebookReport(directory=directory,writeLog=writelog,logFileName=logfilename,overwrite=overwrite,pauseForENV=pauseforenv)

commandLineInterface.add_command(nbReport)

@click.command()
@click.option('--directory',type = str,required = False, default = './',show_default = True, help='The directory to run the notebook report. It will recurse and check all jupyter notebooks in subdirectories.')
@click.option('--writeLog', type = bool, required = False ,default = False,show_default = True, help='This will write the output to a log file. The default value is "False".')
@click.option('--logFileName', type = str, required = False,default = None,show_default = True, help='Use this to change the default name of the log file. The default value is <report_name>.log')
def mdLinkCheck(directory,writelog,logfilename):
    '''Markdown Link Checker.

    This report will check all markdown links to see if they are valid on the file system 
    or if they return a valid status code from a get request. It will check both markdown
    links and html img tag links.
    '''
    MarkdownLinkReport(directory=directory,writeLog=writelog,logFileName=logfilename)

commandLineInterface.add_command(mdLinkCheck)

@click.command()
@click.option('--directory',type = str,required = False, default = './',show_default = True, help='The directory to run the notebook report. It will recurse and check all jupyter notebooks in subdirectories.')
@click.option('--writeLog', type = bool, required = False ,default = False,show_default = True, help='This will write the output to a log file. The default value is "False".')
@click.option('--logFileName', type = str, required = False,default = None,show_default = True, help='Use this to change the default name of the log file. The default value is <report_name>.log')
@click.option('--cSpellConfig',type = str,required = False, default = './cSpell.json',show_default = True, help='''
    Add configuration options to cSpell in this file. The list of ignore words will be included in this file.\n
    Default: 'cSpell.json'\n
    For a complete list of options, please go to:\n
    https://www.npmjs.com/package/cspell#cspelljson


    Example cSpell.json:

    {\n
    "ignoreWords": [\n
        "dtypes",\n
        "iloc",\n
        "numpy",\n
        "Dataframe"\n
        ]\n
    }

    The default config file is expected to be 'cSpell.json'. You may however pass in another config file as long as it's valid json and conforms with the cSpell config json format.

''')
def nbSpellCheck(directory,writelog,logfilename,cspellconfig):
    '''Jupyter Notebook Spell Checker.

    This module parses all notebooks and runs cspell on the code and
    markdown cells. Any misspelled words are added to a set of words.
    This set of words is printed at the very end. It is recommended to
    run this code per unit and update the unit-level spelling dictionary.
    '''
    SpellCheckNotebookReport(directory=directory,writeLog=writelog,logFileName=logfilename,cSpellConfig=cspellconfig)
commandLineInterface.add_command(nbSpellCheck)

#%%
if __name__ == "__main__":
    commandLineInterface()
    # testDir = '/Users/shartley/Documents/trilogyCurriculum/FinTech-Lesson-Plans//01-Lesson-Plans/05-APIs/3/Activities/04-Stu_Three_Stock_Monte/Solved'
    # NotebookReport(directory=testDir,pauseForENV=True,writeLog=False,overwrite=False,logFileName=None)