import pytest
from fdsolver.classes import Relation, FD, FDSet
from fdsolver.io import FDReader
from fdsolver.solver import Solver

@pytest.fixture
def make_solver_1():
    fd_a_b = FD(Relation('A'), Relation('B'))
    fd_b_c = FD(Relation('B'), Relation('C'))
    fd_c_d = FD(Relation('C'), Relation('D'))
    fd_d_e = FD(Relation('D'), Relation('E'))

    fdset_1 = FDSet(fd_a_b, fd_b_c, fd_c_d, fd_d_e)
    solver_1 = Solver(fdset_1)
    return solver_1

@pytest.fixture
def make_solver_2():
    fd_a_b = FD(Relation('A'), Relation('B'))
    fd_bc_e = FD(Relation('BC'), Relation('E'))
    fd_c_d = FD(Relation('C'), Relation('D'))

    fdset_2 = FDSet(fd_a_b, fd_bc_e, fd_c_d)
    solver_2 = Solver(fdset_2)
    return solver_2

@pytest.fixture
def make_solver_3():
    fd_a_b = FD(Relation('A'), Relation('B'))
    fd_bc_e = FD(Relation('BC'), Relation('D'))

    fdset_3 = FDSet(fd_a_b, fd_bc_e)
    solver_3 = Solver(fdset_3)
    return solver_3

@pytest.fixture
def fdsets():
    rel_abc = Relation('ABC')
    rel_cde = Relation('CDE')
    rel_de = Relation('DE')
    rel_bc = Relation('BC')
    rel_ad = Relation('AD')
    rel_b = Relation('B')
    rel_e = Relation('E')
    
    fd_abc_de = FD(rel_abc, rel_de) 
    fd_cde_bc = FD(rel_cde, rel_bc)
    fd_de_b = FD(rel_de, rel_b)
    fd_bc_e = FD(rel_bc, rel_e)
    fd_ad_e = FD(rel_ad, rel_e)

    fdset_1 = FDSet()
    fdset_1.add_step(fd_abc_de)
    fdset_1.add_step(fd_cde_bc)
    fdset_1.add_step(fd_bc_e)
    fdset_1.add_step(fd_ad_e)

    fdset_2 = FDSet() # same as 1
    fdset_2.add_step(fd_abc_de)
    fdset_2.add_step(fd_cde_bc)
    fdset_2.add_step(fd_bc_e)
    fdset_2.add_step(fd_ad_e)
    
    fdset_3 = FDSet()
    fdset_3.add_step(fd_cde_bc)
    fdset_3.add_step(fd_ad_e)
    fdset_3.add_step(fd_de_b)

    return [fdset_1, fdset_2, fdset_3]

