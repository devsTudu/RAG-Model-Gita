import typer
import inquirer
from pyfiglet import Figlet
import pytest

from utils.environmentVariablesHandler import checkValue, VARIABLES
from scripts.DataLoader import load

app = typer.Typer()


TITLE = Figlet("standard").renderText("Gita RAG Model")
print(TITLE)


@app.command()
def set_variables():
    """
    Set the variables required for function of server"""
    for k, v in VARIABLES.items():
        checkValue(k, v)


@app.command()
def upload_info():
    """
    To set up the document storage for retrieval by the model.
    """
    load()


@app.command()
def test_functions():
    """
    Conduct a test to run all the functions
    """
    # pytest.main()
    pass


if __name__ == "__main__":
    app()
