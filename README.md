# FDSolver

FDSolver is a library for solving functional dependencies. Solving refers to things like finding keys, closures, BCNF/3NF checks, and synthesizing BCNF/3NF decompositions.

I made this since there weren't really any similar libraries in Python. The ultimate goal is to make an intuitive and fully-featured set of classes for manipulating relations and functional dependencies, as well as an interface so the features can be used without coding.

## Getting Started
> **Warning:** You're looking at a pre-release version of this library which may contain bugs. Use at your own caution!

Functional dependencies (**FD**) are implemented together with their sets (**FDSet**). It uses Python's built-in sets to
represent relations:
```python
>>> from fdsolver.classes import FD, FDSet

## Make FDs from sets (and strings!)
>>> fd_a_bc = FD(set('A'), set('BC'))
>>> fd_a_bc
A -> B,C
>>> fd_x_yz = FD('X>yZ')                  # Use > as the delimiter
X -> Y,Z                                  # Each char will be taken as an element

## A wide set of built-in functionality
>>> fd_a_bc.decompose()                   # Returns a FDSet (see below)
A -> C
A -> B

>>> fd_a_b, fd_a_c = fd_a_bc.decompose()  # Union operator
>>> fd_a_b | fd_a_c
A -> C,B

>>> fd_a_bc.augment(set('D'))             # Augmentation returns a new FD
A,D -> B,C,D
>>> fd_a_bc.augment('EF')                 # Accepts characters
A,D,E,F -> B,C,D,E,F

>>> FD('AB>AC').untrivialize()            # Removes trivial elements from RHS
A,B -> C

>>> FD('A>B').is_contained_in(fd_a_bc)    # Is one FD a subset of another?
True

## Make FDSets from FDs
>>> fdset_1 = FDSet(FD('A>B'), FD('A>C'), FD('A>D'))
>>> fdset_1
A -> B
A -> C
A -> D
>>> fdset_1.add_step(FD('A>E'))
>>> fdset_1
A -> B
A -> C
A -> D
A -> E
```
**Solvers** are a separate class from the FDSet class to abstract out the solver logic. There is also a reader class (**FDReader**) and a writer class (**FDWriter**) to make IO easier.
```python
>>> from fdsolver.classes import FD, FDSet
>>> from fdsolver.solver import Solver
>>> from fdsolver.io import FDReader, FDWriter

## Create solvers from FDSets
>>> fdset = ...
>>> solver = Solver(fdset)
>>> solver
A,B,D -> E
A,C,E -> A,D
B,D -> E
C,D -> B,E
C,E -> B,D

## Find closures, keys, and more
>>> solver.closure(set('CE'))
r{B,C,D,E}
>>> solver.keys()
[r{A,C,D}, r{A,C,E}]
>>> solver.superkeys()
[r{A,C,D}, r{A,C,E}, r{A,B,C,D}, r{A,B,C,E}, r{A,C,D,E}, r{A,B,C,D,E}]
>>> solver.prime_attrs()
r{A,C,D,E}

## BCNF functionality is included
>>> solver.is_bcnf(set('ACE'))
True
>>> solver.find_bcnf_decomp(set('ABCDE'))
[r{B,D,E}, r{B,C,D}, r{A,C,E}]

## Verify if two relations can be losslessly joined
>>> solver.is_lossless_decomp(set('BDE'), set('BCD'))
True

```

## Features

Current feature checklist:
- [x] set class with Pythonic operators
- [x] Functional dependency (FD) class with Pythonic operators
- [x] Set of functional dependencies (FDSet) class with Pythonic operators
- [x] Basic FD functionality like decomposition, augmentation, subsets
- [ ] Solver functions:
    - [x] Keys, subkeys, prime attributes
    - [x] Closures
    - [x] Check whether a relation is in BCNF
    - [x] Finding BCNF decompositions
    - [x] Checking whether a decomposition is lossless
    - [x] Check whether a relation is in 3NF
    - [x] Finding minimal bases
    - [ ] Performing 3NF synthesis
- [ ] Make the code more intuitive to write
- [ ] User friendly interface (GUI? Web app?)
- [ ] Launching on Pip?

## Project Structure
```
(root dir)
├── CHANGELOG.md
├── LICENSE.txt
├── README.md
├── setup.py
├── fdsolver
│   ├── __init__.py
│   ├── classes.py
│   ├── graph.py (WIP)
│   ├── io.py
│   └── solver.py
└── tests
    ├── fixtures.py
    ├── test_basic_functionality.py
    ├── test_data
    │   ├── test_data_1.txt
    │   └── test_data_2.txt
    ├── test_io.py
    ├── test_operations.py
    └── test_solver.py
```

## Tests
Currently, this library uses [Pytest](https://docs.pytest.org/en/6.2.x/) to perform unit testing. The tests are split into different files sorted according to what they are testing.

Coverage isn't amazing, but it ensures that there are no show-stopping bugs that either lead to crashes or obviously wrong answers. At this point, I'm not sure if it can catch more subtle bugs, but I'll just have to wait and see.

## Usage
Since this project isn't launched on Pip yet, just clone it and do `pip install -e .` in the root directory.

From there, you can start importing and using the library with `from fdsolver.classes import *` and so on.

