import pytest
from fdsolver.classes import FD, FDSet
from fdsolver.io import FDReader
from fdsolver.solver import Solver

@pytest.fixture
def make_solver_1():
    fd_a_b = FD(set('A'), set('B'))
    fd_b_c = FD(set('B'), set('C'))
    fd_c_d = FD(set('C'), set('D'))
    fd_d_e = FD(set('D'), set('E'))

    fdset_1 = FDSet(fd_a_b, fd_b_c, fd_c_d, fd_d_e)
    solver_1 = Solver(fdset_1)
    return solver_1

@pytest.fixture
def make_solver_2():
    fd_a_b = FD(set('A'), set('B'))
    fd_bc_e = FD(set('BC'), set('E'))
    fd_c_d = FD(set('C'), set('D'))

    fdset_2 = FDSet(fd_a_b, fd_bc_e, fd_c_d)
    solver_2 = Solver(fdset_2)
    return solver_2

@pytest.fixture
def make_solver_3():
    fd_a_b = FD(set('A'), set('B'))
    fd_bc_e = FD(set('BC'), set('D'))

    fdset_3 = FDSet(fd_a_b, fd_bc_e)
    solver_3 = Solver(fdset_3)
    return solver_3

@pytest.fixture
def make_solver_4():
    fd_abd_e = FD(set('ABD'), set('E'))
    fd_acd_ad = FD(set('ACE'), set('AD'))
    fd_bd_e = FD(set('BD'), set('E'))
    fd_cd_be = FD(set('CD'), set('BE'))
    fd_ce_bd = FD(set('CE'), set('BD'))
    
    fdset_4 = FDSet(fd_abd_e, fd_acd_ad, fd_bd_e, fd_cd_be, fd_ce_bd)
    solver_4 = Solver(fdset_4)
    return solver_4

@pytest.fixture
def fdsets():
    rel_abc = set('ABC')
    rel_cde = set('CDE')
    rel_de = set('DE')
    rel_bc = set('BC')
    rel_ad = set('AD')
    rel_b = set('B')
    rel_e = set('E')
    
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

