from setuptools import setup,find_packages

setup(
    name="qaSuite",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'bs4',
        'nbconvert',
        'requests',
        'click',
        'progressbar2'
    ],
    py_modules=['QaSuite','NotebookReport','MarkdownLinkReport','SpellCheckNotebookReport','ReportBase','ErrorBase'],
    entry_points='''
        [console_scripts]
        qaSuite=QaSuite:commandLineInterface
    ''',
)