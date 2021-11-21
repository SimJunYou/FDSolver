from time import sleep
from fdsolver.classes import FD, FDSet
from rich.console import Console, Group
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.markdown import Markdown
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt, IntPrompt

WELCOME = """
# Welcome to FDSolver v0.2!
**Solver for Functional Dependencies.**  
Make FDs, find closures, BCNF/3NF, and more.  
*This is an alpha version - expect bugs!*  
Made by Sim Jun You, 2021
"""
INSTRUCTIONS = """
1. Make a new set of FDs
2. Find the closure of a FD set
3. Find the BCNF decomp of an FD set
4. *Quit*
"""

NEW_FDSET, CLOSURE, BCNF_DECOMP, QUIT = range(1,5)
MAIN_CHOICES = list(map(str, range(1,5)))

def entry():
    console, layout = Console(), initialize_layout()
    objs, res, choice = {}, None, None
    with console.screen() as screen:
        while choice != QUIT: # Main loop
            ### Update visuals
            if res:
                layout['display'].update(res)
                layout['instructions'].visible = False
            elif objs:
                renderedObjs = render_objs(objs)
                layout['display'].update(renderedObjs)

            ### Render visuals
            screen.update(layout)

            ### User input and updating of objects
            if res:
                wait_for_user()
                res = None
                layout['instructions'].visible = True
            else:
                choice = show_menu()
            
            objs, res = handle_choice(choice, objs)

            ### Refresh again to remove prompts
            screen.update(layout)

def handle_choice(choice, objs):
    if choice == NEW_FDSET:
        name = Prompt.ask("Name of new FD set")
        fds = Prompt.ask("New FD set + name in the form 'AB>CD;CD>E'")
        newFdSet = FDSet([FD(eachFdStr) for eachFdStr in fds.split(';')])
        objs[name] = newFdSet
        res = [] # no results
    return objs, []

def render_objs(objs):
    renderGroup = []
    for eachFdSetName, eachFdSet in objs.items():
        if not isinstance(eachFdSet, FDSet): 
            continue # not supported
        currTable = Table()
        currTable.add_column(eachFdSetName)
        for eachFd in eachFdSet:
            currTable.add_row(Text(str(eachFd)))
        renderGroup.append(currTable)
    return Group(*renderGroup)

def show_menu():
    user = IntPrompt.ask("[bold yellow]Next action:[/bold yellow]", choices=MAIN_CHOICES)
    return user

def wait_for_user():
    Prompt.ask("Press enter to continue")

def initialize_layout():
    layout = Layout()
    title, instructions, welcome = get_title_instr_welcome()
    
    layout.split_column(
        Layout(title, name='title', size=3),
        Layout(name='body')
    )
    layout['body'].split_column(
        Layout(welcome, name='display'),
        Layout(instructions, name='instructions', size=len(MAIN_CHOICES)+1)
    )
    
    return layout

def get_title_instr_welcome():
    title = Align.center(
        Text.from_markup(f"[green bold underline]FDSolver v0.2[/green bold underline]", justify="center"),
        vertical="middle",
    )
    instructions = Align.center(
        Markdown(INSTRUCTIONS),
    )
    welcome = Align.center(
        Markdown(WELCOME, justify="center"),
        vertical="middle",
        width=50
    )
    return title, instructions, welcome


def update_tables(objs):
    '''
    Updates tables based on current FD objects stored
    '''
    return [Table()]

