# Qa Suite

This is the QA Suite of Tools.

  It contains:

  Notebook Report       - Runs all jupyter notebooks and checks for errors.
  Markdown Link Checker - Checks that all markdown links are valid.

## Installation

```shell
pip install -e .
```

## qaSuite Help

```shell
qaSuite --help
Usage: qaSuite [command] [options]

Options:
  --help  Show this message and exit.

Commands:
  mdlinkcheck  Markdown Link Checker.
  nbreport     Notebook Report.
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
  --directory TEXT  The directory to run the link checker. It will recurse and
                    check all markdown files in subdirectories.

  --help            Show this message and exit.

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
  --directory TEXT  The directory to run the notebook report. It will recurse
                    and check all jupyter notebooks in subdirectories.

  --kernel TEXT     This is the kernel to use when parsing the notebook.
                    Default: "python3"

  --overwrite TEXT  Enabling this will overwrite the notebook with the output
                    of the report.

  --help            Show this message and exit.
```