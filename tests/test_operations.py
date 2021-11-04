import pytest
from fdsolver.classes import *
from tests.fixtures import all_objs

def test_relation_equality(all_objs):
    rel_abc = all_objs['rel_abc']
    rel_abc2 = all_objs['rel_abc2']
    rel_de = all_objs['rel_de']

    assert rel_abc == rel_abc2
    assert rel_abc != rel_de

def test_relation_union(all_objs):
    rel_abc = all_objs['rel_abc']
    rel_ad = all_objs['rel_ad']

    assert rel_abc | rel_ad == Relation('ABCD')
    rel_abc |= rel_ad
    assert rel_abc == Relation('ABCD')

def test_relation_intersect(all_objs):
    rel_abc = all_objs['rel_abc']
    rel_ad = all_objs['rel_ad']

    assert rel_abc & rel_ad == Relation('A')
    rel_abc &= rel_ad
    assert rel_abc == Relation('A')

def test_relation_difference(all_objs):
    rel_abc = all_objs['rel_abc']
    rel_ad = all_objs['rel_ad']

    assert rel_abc - rel_ad == Relation('BC')
    rel_abc -= rel_ad
    assert rel_abc == Relation('BC')

def test_relation_string(all_objs):
    rel_abc = all_objs['rel_abc']
    rel_d = all_objs['rel_d']
    rel_d.name = 'R2'

    assert str(rel_abc) == "r{A,B,C}"
    assert str(rel_d) == "R2{D}"

def test_fd_equality(all_objs):
    fd_abc_de = all_objs['fd_abc_de']
    fd_abc_de2 = all_objs['fd_abc_de2']
    fd_abc_e = all_objs['fd_abc_e']
    fd_abc_cde = all_objs['fd_abc_cde']
    fd_de_b = all_objs['fd_de_b']

    assert fd_abc_de == fd_abc_de2
    assert fd_abc_e != fd_abc_de
    assert fd_abc_de != fd_abc_cde
    assert fd_de_b != fd_abc_e

def test_fd_string(all_objs):
    fd_abc_de = all_objs['fd_abc_de']
    fd_abc_de2 = all_objs['fd_abc_de2']
    fd_abc_e = all_objs['fd_abc_e']
    fd_abc_cde = all_objs['fd_abc_cde']
    fd_de_b = all_objs['fd_de_b']

    assert str(fd_abc_de) == "r{A,B,C} -> r{D,E}"
    assert str(fd_de_b) == "r{D,E} -> r{B}"

def test_fdset_equality(all_objs):
    fdset_1 = all_objs['fdset_1']
    fdset_2 = all_objs['fdset_2']
    fdset_3 = all_objs['fdset_3']

    assert fdset_1 == fdset_2
    assert fdset_2 == fdset_1
    assert fdset_1 != fdset_3
    assert fdset_2 != fdset_3

def test_fdset_indexing(all_objs):
    fdset_1 = all_objs['fdset_1']
    fd_cde_bc = all_objs['fd_cde_bc']
    fdset_3 = all_objs['fdset_3']
    fd_de_b = all_objs['fd_de_b']

    assert fdset_1[1] == fd_cde_bc
    assert fdset_3[-1] == fd_de_b 

def test_fdset_contains(all_objs):
    fdset_1 = all_objs['fdset_1']
    fd_cde_bc = all_objs['fd_cde_bc']
    fdset_3 = all_objs['fdset_3']
    fd_de_b = all_objs['fd_de_b']

    assert fd_cde_bc in fdset_1
    assert fd_de_b in fdset_3 
