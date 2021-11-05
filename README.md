# FDSolver

FDSolver is a library for solving functional dependencies. Solving refers to things like finding keys, closures, BCNF/3NF checks, and synthesizing BCNF/3NF decompositions.

I made this since there weren't really any similar libraries in Python. The ultimate goal is to make an intuitive and fully-featured set of classes for manipulating relations and functional dependencies, as well as an interface so the features can be used without coding.

## Getting Started
> **Warning:** You're looking at a pre-release version of this library which may contain bugs. Use at your own caution!

The **Relation** class has complete functionality:
```python
>>> from fdsolver.classes import Relation

## Fast creation and naming
## The relation constructor takes any iterable as the element set, but characters are recommended
>>> rel_abc = Relation('ABC')
>>> rel_abc
r{A,B,C}
>>> rel_abc.name = 'R1'
>>> rel_abc
R1{A,B,C}
>>> rel_def = Relation('DEF', name='R2')
>>> rel_def
R2{D,E,F}

## Intuitive iteration
>>> for each_rel in Relation('DEF'):
...     print(each_rel)             
r{F}
r{E}
r{D}

## Wide variety of operator implementations
>>> Relation('AB') in Relation('ABCD') # Subset (non-strict)
True
>>> Relation('DE') in Relation('ABCD')
False
>>> Relation('AB') | Relation('AC')    # Union
r{A,B,C}
>>> Relation('AB') & Relation('AC')    # Intersect
r{A}
>>> Relation('AB') - Relation('AC')    # Difference
r{B}

## Conveniently find all subsets
>>> print(rel_abc.subsets())
[r{C}, r{B}, r{A}, r{B,C}, r{A,C}, r{A,B}, r{A,B,C}]
```

Functional dependencies (**FD**) are implemented together with their sets (**FDSet**), built on top of the Relation class:
```python
>>> from fdsolver.classes import Relation, FD, FDSet

## Make FDs from Relations
>>> fd_a_bc = FD(Relation('A'), Relation('BC'))
>>> fd_a_bc
r{A} -> r{B,C}

## A wide set of built-in functionality
>>> fd_a_bc.decompose()                   # Returns a FDSet
r{A} -> r{C}
r{A} -> r{B}

>>> fd_a_b, fd_a_c = fd_a_bc.decompose()  # Union operator
>>> fd_a_b | fd_a_c
r{A} -> r{C,B}

>>> fd_a_bc.augment(Relation('D'))        # In-place augmentation
>>> fd_a_bc
r{A,D} -> r{B,C,D}
>>> fd_a_bc.unaugment()
>>> fd_a_bc
r{A} -> r{B,C}

## Make FDSets from FDs
>>> fdset_1 = FDSet(fd_a_b, fd_a_c, FD(Relation('A'), Relation('D')))
>>> fdset_1
r{A} -> r{D}
r{A} -> r{C}
r{A} -> r{B}
>>> fdset_1.add_step(FD(Relation('A'), Relation('E')))
>>> fdset_1
r{A} -> r{E}
r{A} -> r{D}
r{A} -> r{C}
r{A} -> r{B}
```
**Solvers** are a separate class from the FDSet class despite having practically the same properties. This is to separate the solver logic from the core code of the FDSet class. There is also a reader class (**FDReader**) and a writer class (**FDWriter**) to make IO easier.
```python
>>> from fdsolver.classes import Relation, FD, FDSet
>>> from fdsolver.solver import Solver
>>> from fdsolver.io import FDReader, FDWriter

## Create solvers from FDSets
>>> fdset_1 = ...
>>> solver1 = Solver(fdset_1)

## ... or directly create objects from file inputs
>>> reader = FDReader('input.txt')
>>> solver = reader.get_solver()
>>> solver
r{A,B,D} -> r{E}
r{A,C,E} -> r{A,D}
r{B,D} -> r{E}
r{C,D} -> r{B,E}
r{C,E} -> r{B,D}

## Find closures, keys, and more
>>> solver.closure(Relation('CE'))
r{B,C,D,E}
>>> solver.keys()
[r{A,C,D}, r{A,C,E}]
>>> solver.superkeys()
[r{A,C,D}, r{A,C,E}, r{A,B,C,D}, r{A,B,C,E}, r{A,C,D,E}, r{A,B,C,D,E}]
>>> solver.prime_attrs()
r{A,C,D,E}

## BCNF functionality is included
>>> solver.is_bcnf(Relation('ACE'))
True
>>> solver.find_bcnf_decomp(Relation('ABCDE'))
[r{B,D,E}, r{B,C,D}, r{A,C,E}]

## Verify if two relations can be losslessly joined
>>> solver.is_lossless_decomp(Relation('BDE'), Relation('BCD'))
True

```

## Features

Current feature checklist:
- [x] Relation class with Pythonic operators
- [x] Functional dependency (FD) class with Pythonic operators
- [x] Set of functional dependencies (FDSet) class with Pythonic operators
- [x] Basic FD functionality like decomposition, augmentation, subsets
- [ ] Solver functions:
    - [x] Keys, subkeys, prime attributes
    - [x] Closures
    - [x] Check whether a relation is in BCNF
    - [x] Finding BCNF decompositions
    - [x] Checking whether a decomposition is lossless
    - [ ] Check whether a relation is in 3NF
    - [ ] Finding minimal bases
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

