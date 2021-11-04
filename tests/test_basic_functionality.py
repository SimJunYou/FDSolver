import pytest
from fdsolver.classes import Relation, FD, FDSet

def test_rel_is_subset():
    rel_abc = Relation('ABC') 
    rel_cde = Relation('CDE')
    rel_de = Relation('DE')

    assert not (rel_de in rel_abc)
    assert rel_de in rel_cde
    assert rel_cde in rel_cde

def test_rel_generate_subsets():
    rel_abc = Relation('ABC') 
    subsets = rel_abc.subsets()
    assert Relation('A') in subsets
    assert Relation('B') in subsets
    assert Relation('C') in subsets
    assert Relation('AB') in subsets
    assert Relation('AC') in subsets
    assert Relation('BC') in subsets
    assert Relation('ABC') in subsets
    assert len(subsets) == 7

def test_fd_decomposition():
    fd_abc_de = FD(Relation('ABC'), Relation('DE'))
    fd_abc_d = FD(Relation('ABC'), Relation('D'))
    fd_abc_e = FD(Relation('ABC'), Relation('E'))
    
    decomposed = fd_abc_de.decompose()
    fdset_2 = FDSet(fd_abc_d, fd_abc_e)
    assert decomposed == fdset_2

def test_fd_union():
    fd_abc_de = FD(Relation('ABC'), Relation('DE'))
    fd_abc_d = FD(Relation('ABC'), Relation('D'))
    fd_abc_e = FD(Relation('ABC'), Relation('E'))
    
    unioned = fd_abc_d | fd_abc_e
    assert unioned == fd_abc_de


