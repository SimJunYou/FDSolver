import pytest
from fdsolver.classes import *

@pytest.fixture
def all_objs():
    rel_abc = Relation('ABC')
    rel_abc2 = Relation('ABC')
    rel_cde = Relation('CDE')

    # Testing fileInput parameter
    rel_de = Relation(None, fileInput='{D,E}')
    rel_bc = Relation(None, fileInput='{B,C}')
    rel_ad = Relation(None, fileInput='{A,D}')

    rel_a = Relation('A')
    rel_b = Relation('B')
    rel_c = Relation('C')
    rel_d = Relation('D')
    rel_e = Relation('E')
    
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

    return dict(**locals())

