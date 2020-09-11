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
    ],
    py_modules=['QaSuite','NotebookReport','MarkdownLinkReport'],
    entry_points='''
        [console_scripts]
        qaSuite=QaSuite:commandLineInterface
    ''',
)