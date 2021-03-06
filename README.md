# Qa Suite

This is the QA Suite of Tools.

  It contains:

  Notebook Report       - Runs all jupyter notebooks and checks for errors.
  Markdown Link Checker - Checks that all markdown links are valid.
  Notebook Spell Checker - Checks the spelling in all markdown and code cells for a jupyter notebook.

## Installation

```shell
pip install .
```

## qaSuite Help

```shell
qaSuite --help
Usage: qaSuite [command] [options]

Options:
  --help  Show this message and exit.

Commands:
  mdlinkcheck   Markdown Link Checker.
  nbreport      Notebook Report.
  nbspellcheck  Jupyter Notebook Spell Checker.
```

# Markdown link checker
Markdown Link Checker.

  This report will check all markdown links to see if they are valid on the
  file system  or if they return a valid status code from a get request. It
  will check both markdown links and html img tag links.
## mdlinkcheck Help
```shell 
qaSuite mdlinkcheck --help

Options:
  --directory TEXT    The directory to run the notebook report. It will
                      recurse and check all jupyter notebooks in
                      subdirectories.  [default: ./]

  --writeLog BOOLEAN  This will write the output to a log file. The default
                      value is "False".  [default: False]

  --logFileName TEXT  Use this to change the default name of the log file. The
                      default value is <report_name>.log

  --help              Show this message and exit.

```

# Notebook Report


  Notebook Report.

  The Notebook Report will recurse a directory and check all .ipynb files
  using the nbconvert ExecutionPreprocessor.  It will save the output to the
  same file name and will list all failing notebooks as well as their cells
  that failed with the associated stack trace.

## nbreport Help

```shell
qaSuite nbreport --help

Options:
  --directory TEXT       The directory to run the notebook report. It will
                         recurse and check all jupyter notebooks in
                         subdirectories.  [default: ./]

  --writeLog BOOLEAN     This will write the output to a log file. The default
                         value is "False".  [default: False]

  --logFileName TEXT     Use this to change the default name of the log file.
                         The default value is <report_name>.log

  --overwrite BOOLEAN    Enabling this will overwrite the notebook with the
                         output of the report.  [default: False]

  --pauseForENV BOOLEAN  Enabling this will pause execution if a missing
                         environment variable is found. The user will have a
                         chance to enter the variable and rerun the report.
                         [default: False]

  --help                 Show this message and exit.
```

# Notebook Spell Check Report

  This module parses all notebooks and runs cspell on the code and
  markdown cells. Any misspelled words are added to a set of words.
  This set of words is printed at the very end. It is recommended to
  run this code per unit and update the unit-level spelling dictionary.

> **Note**: This report requires that cSpell be installed on your system. Please follow the [installation instructions](https://www.npmjs.com/package/cspell) on the cSpell page if you need to install it.
## nbspellcheck Help

```shell
Options:
  --directory TEXT     The directory to run the notebook report. It will
                       recurse and check all jupyter notebooks in
                       subdirectories.  [default: ./]

  --writeLog BOOLEAN   This will write the output to a log file. The default
                       value is "False".  [default: False]

  --logFileName TEXT   Use this to change the default name of the log file.
                       The default value is <report_name>.log

  --cSpellConfig TEXT  Add configuration options to cSpell in this file. The
                       list of ignore words will be included in this file.
                       
                       Default: 'cSpell.json'
                       
                       For a complete list of options, please go to:
                       
                       https://www.npmjs.com/package/cspell#cspelljson
                       
                       Example cSpell.json:
                       
                       {
                       
                       "ignoreWords": [
                       
                           "dtypes",
                       
                           "iloc",
                       
                           "numpy",
                       
                           "Dataframe"
                       
                           ]
                       
                       }
                       
                       The default config file is expected to be
                       'cSpell.json'. You may however pass in another config
                       file as long as it's valid json and conforms with the
                       cSpell config json format.  [default: ./cSpell.json]

  --help               Show this message and exit.
```