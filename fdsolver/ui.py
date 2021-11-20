from time import sleep

from fdsolver.classes import FD, FDSet

from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.markdown import Markdown
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import IntPrompt

HELPTEXT = """
# Welcome to FDSolver v0.2

1. Make a new set of FDs
2. Find the closure of a FD set
3. Find the BCNF decomp of an FD set
"""

def entry():
    console = Console()
    layout = Layout()
    choice = ["New FD"]
    objs = []
    user = None

    with console.screen() as screen:
        title = Align.center(
            Text.from_markup(f"[green bold underline]FDSolver v0.2[/green bold underline]", justify="center"),
            vertical="middle",
        )
        layout.split_column(
            Layout(name='title', size=3),
            Layout(name='body', size=console.height-3)
        )
        while user != 3:
            if not objs:
                helpText = Align.center(
                    Markdown(HELPTEXT),
                    vertical="middle",
                    width=50
                )
                layout['title'].update(title)
                layout['body'].update(helpText)

            screen.update(layout)
            user = menu()

NEW_FDSET   = 1
CLOSURE     = 2
BCNF_DECOMP = 3

MAIN_CHOICES = list(map(str, range(1,4)))
def menu():
    user = IntPrompt.ask("[yellow]Next action:[/yellow]", choices=MAIN_CHOICES, default=1)
    return user
    

def update_tables(objs):
    '''
    Updates tables based on current FD objects stored
    '''
    return [Table()]

