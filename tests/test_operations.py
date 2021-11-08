import pytest
from fdsolver.classes import FD, FDSet
from tests.fixtures import fdsets

def test_fd_equality():
    rel_abc = set('ABC')
    rel_cde = set('CDE')
    rel_ad = set('AD')
    rel_de = set('DE')
    rel_b = set('B')
    rel_e = set('E')

    fd_abc_de = FD(rel_abc, rel_de)
    fd_abc_de2 = FD(rel_abc, rel_de)
    fd_abc_e = FD(rel_abc, rel_e)
    fd_abc_cde = FD(rel_abc, rel_cde)
    fd_de_b = FD(rel_de, rel_b) 

    assert fd_abc_de == fd_abc_de2
    assert fd_abc_e != fd_abc_de
    assert fd_abc_de != fd_abc_cde
    assert fd_de_b != fd_abc_e

def test_fdset_equality(fdsets):
    fdset_1, fdset_2, fdset_3 = fdsets

    assert fdset_1 == fdset_2
    assert fdset_2 == fdset_1
    assert fdset_1 != fdset_3
    assert fdset_2 != fdset_3

def test_fdset_indexing(fdsets):
    fdset_1, _, fdset_3 = fdsets
    fd_cde_bc = FD(set('CDE'), set('BC'))
    fd_de_b = FD(set('DE'), set('B'))

    assert fdset_1[1] == fd_cde_bc
    assert fdset_3[-1] == fd_de_b 

def test_fdset_contains(fdsets):
    fdset_1, _, fdset_3 = fdsets
    fd_cde_bc = FD(set('CDE'), set('BC'))
    fd_de_b = FD(set('DE'), set('B'))

    assert fd_cde_bc in fdset_1
    assert fd_de_b in fdset_3 
