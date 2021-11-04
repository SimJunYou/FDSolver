import pytest
from fdsolver.classes import *

@pytest.fixture
def relations():
    rel_abc = Relation('ABC')
    rel_abc2 = Relation('ABC')
    rel_cde = Relation('CDE')

    rel_de = Relation('DE')
    rel_bc = Relation('BC')
    rel_ad = Relation('AD')

    rel_a = Relation('A')
    rel_b = Relation('B')
    rel_c = Relation('C')
    rel_d = Relation('D')
    rel_e = Relation('E')
    
    return dict(**locals())

def test_relation_instancing(relations):
    pass

@pytest.fixture
def fds(relations):
    rel_abc = relations['rel_abc']
    rel_abc2 = relations['rel_abc2']
    rel_cde = relations['rel_cde']
    rel_de = relations['rel_de']
    rel_bc = relations['rel_bc']
    rel_ad = relations['rel_ad']
    rel_b = relations['rel_b']
    rel_c = relations['rel_c']
    rel_d = relations['rel_d']
    rel_e = relations['rel_e']
    
    fd_abc_abc2 = FD(rel_abc, rel_abc2)
    fd_abc_cde = FD(rel_abc, rel_cde)

    fd_abc_de = FD(rel_abc, rel_de) 
    fd_abc_d = FD(rel_abc, rel_d)
    fd_abc_e = FD(rel_abc, rel_e)
    fd_abc_de2 = FD(rel_abc, rel_de)

    fd_cde_bc = FD(rel_cde, rel_bc)
    
    fd_de_b = FD(rel_de, rel_b)
    fd_de_c = FD(rel_de, rel_c)
    fd_bc_e = FD(rel_bc, rel_e)
    fd_ad_e = FD(rel_ad, rel_e)

    return dict(**locals())

def test_fds_instancing(fds):
    pass

@pytest.fixture
def fdsets(fds):
    fd_abc_de = fds['fd_abc_de']
    fd_cde_bc = fds['fd_cde_bc']
    fd_bc_e   = fds['fd_bc_e']
    fd_ad_e   = fds['fd_ad_e']
    
    fdset_1 = FDSet()
    fdset_1.add_step(fd_abc_de)
    fdset_1.add_step(fd_cde_bc)
    fdset_1.add_step(fd_bc_e)
    fdset_1.add_step(fd_ad_e)

    return dict(**locals())

def test_fdset_instancing(fdsets):
    pass

def test_relation_equality(relations):
    rel_abc = relations['rel_abc']
    rel_abc2 = relations['rel_abc2']
    rel_de = relations['rel_de']

    assert rel_abc == rel_abc2
    assert rel_abc != rel_de

def test_fd_equality(fds):
    fd_abc_de = fds['fd_abc_de']
    fd_abc_de2 = fds['fd_abc_de2']
    fd_abc_e = fds['fd_abc_e']
    fd_abc_cde = fds['fd_abc_cde']
    fd_de_b = fds['fd_de_b']

    assert fd_abc_de == fd_abc_de2
    assert fd_abc_e != fd_abc_de
    assert fd_abc_de != fd_abc_cde
    assert fd_de_b != fd_abc_e

def test_fd_decomposition(fds):
    fd_abc_de = fds['fd_abc_de'] 
    fd_abc_d = fds['fd_abc_d']
    fd_abc_e = fds['fd_abc_e']




    
    
