import pytest
from fdsolver.classes import Relation, FD, FDSet
from tests.fixtures import fdsets

def test_relation_equality():
    rel_abc = Relation('ABC')
    rel_abc2 = Relation('ABC')
    rel_de = Relation('DE')

    assert rel_abc == rel_abc2
    assert rel_abc != rel_de

def test_relation_union():
    rel_abc = Relation('ABC')
    rel_ad = Relation('AD') 

    assert rel_abc | rel_ad == Relation('ABCD')
    rel_abc |= rel_ad
    assert rel_abc == Relation('ABCD')

def test_relation_intersect():
    rel_abc = Relation('ABC')
    rel_ad = Relation('AD')

    assert rel_abc & rel_ad == Relation('A')
    rel_abc &= rel_ad
    assert rel_abc == Relation('A')

def test_relation_difference():
    rel_abc = Relation('ABC')
    rel_ad = Relation('AD')

    assert rel_abc - rel_ad == Relation('BC')
    rel_abc -= rel_ad
    assert rel_abc == Relation('BC')

def test_relation_string():
    rel_abc = Relation('ABC')
    rel_d = Relation('D')
    rel_d.name = 'R2'

    assert str(rel_abc) == "r{A,B,C}"
    assert str(rel_d) == "R2{D}"

def test_fd_equality():
    rel_abc = Relation('ABC')
    rel_cde = Relation('CDE')
    rel_ad = Relation('AD')
    rel_de = Relation('DE')
    rel_b = Relation('B')
    rel_e = Relation('E')

    fd_abc_de = FD(rel_abc, rel_de)
    fd_abc_de2 = FD(rel_abc, rel_de)
    fd_abc_e = FD(rel_abc, rel_e)
    fd_abc_cde = FD(rel_abc, rel_cde)
    fd_de_b = FD(rel_de, rel_b) 

    assert fd_abc_de == fd_abc_de2
    assert fd_abc_e != fd_abc_de
    assert fd_abc_de != fd_abc_cde
    assert fd_de_b != fd_abc_e

def test_fd_string():
    rel_abc = Relation('ABC')
    rel_de = Relation('DE')
    rel_b = Relation('B')

    fd_abc_de = FD(rel_abc, rel_de)
    fd_de_b = FD(rel_de, rel_b) 

    assert str(fd_abc_de) == "r{A,B,C} -> r{D,E}"
    assert str(fd_de_b) == "r{D,E} -> r{B}"

def test_fdset_equality(fdsets):
    fdset_1, fdset_2, fdset_3 = fdsets

    assert fdset_1 == fdset_2
    assert fdset_2 == fdset_1
    assert fdset_1 != fdset_3
    assert fdset_2 != fdset_3

def test_fdset_indexing(fdsets):
    fdset_1, _, fdset_3 = fdsets
    fd_cde_bc = FD(Relation('CDE'), Relation('BC'))
    fd_de_b = FD(Relation('DE'), Relation('B'))

    assert fdset_1[1] == fd_cde_bc
    assert fdset_3[-1] == fd_de_b 

def test_fdset_contains(fdsets):
    fdset_1, _, fdset_3 = fdsets
    fd_cde_bc = FD(Relation('CDE'), Relation('BC'))
    fd_de_b = FD(Relation('DE'), Relation('B'))

    assert fd_cde_bc in fdset_1
    assert fd_de_b in fdset_3 
