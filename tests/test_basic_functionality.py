import pytest
from fdsolver.classes import *
from tests.fixtures import all_objs

def test_rel_subset(all_objs):
    rel_abc = all_objs['rel_abc']
    rel_cde = all_objs['rel_cde']
    rel_de = all_objs['rel_de']

    assert not (rel_de in rel_abc)
    assert rel_de in rel_cde
    assert rel_cde in rel_cde

def test_fd_decomposition(all_objs):
    fd_abc_de = all_objs['fd_abc_de'] 
    fd_abc_d = all_objs['fd_abc_d']
    fd_abc_e = all_objs['fd_abc_e']
    
    decomposed = fd_abc_de.decompose()
    fdset_2 = FDSet(fd_abc_d, fd_abc_e)
    assert decomposed == fdset_2

def test_fd_union(all_objs):
    fd_abc_de = all_objs['fd_abc_de'] 
    fd_abc_d = all_objs['fd_abc_d']
    fd_abc_e = all_objs['fd_abc_e']
    
    unioned = fd_abc_d | fd_abc_e
    assert unioned == fd_abc_de


