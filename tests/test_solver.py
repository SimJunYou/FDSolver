import pytest
from fdsolver.classes import Relation, FD, FDSet
from fdsolver.solver import Solver
from fdsolver.io import FDReader
from tests.fixtures import make_solver_1, make_solver_2, make_solver_3

def test_solver_closure(make_solver_1, make_solver_2):
    solver_1 = make_solver_1
    
    rel_a = Relation('A')
    rel_b = Relation('B')
    rel_c = Relation('C')
    rel_d = Relation('D')
    rel_e = Relation('E')

    assert solver_1.closure(rel_a) == Relation('ABCDE')
    assert solver_1.closure(rel_b) == Relation('BCDE')
    assert solver_1.closure(rel_c) == Relation('CDE')
    assert solver_1.closure(rel_d) == Relation('DE')
    assert solver_1.closure(rel_e) == Relation('E')

    solver_2 = make_solver_2

    assert solver_2.closure(rel_a) == Relation('AB')
    assert solver_2.closure(Relation('AC')) == Relation('ABCDE')
    assert solver_2.closure(Relation('AC'), no_trivial=True) == Relation('BDE')
    assert solver_2.closure(rel_b) == Relation('B')


def test_solver_superkeys(make_solver_2):
    solver_2 = make_solver_2
    rel_abcde = Relation('ABCDE')
    sol2_sk = solver_2.superkeys(rel_abcde)
    assert Relation('ABCDE') in sol2_sk
    assert Relation('ABCD') in sol2_sk
    assert Relation('ABCE') in sol2_sk
    assert Relation('ABC') in sol2_sk
    assert Relation('ACDE') in sol2_sk
    assert Relation('ACD') in sol2_sk
    assert Relation('ACE') in sol2_sk
    assert Relation('AC') in sol2_sk
    assert len(sol2_sk) == 8

def test_solver_keys(make_solver_2):
    solver_2 = make_solver_2
    rel_abcde = Relation('ABCDE')
    sol2_keys = solver_2.keys(rel_abcde)
    assert sol2_keys[0] == Relation('AC')
    assert len(sol2_keys) == 1

def test_solver_prime_attrs(make_solver_2):
    solver_2 = make_solver_2
    rel_abcde = Relation('ABCDE')
    assert solver_2.prime_attrs(rel_abcde) == Relation('AC')
    
def test_solver_is_bcnf(make_solver_3):
    solver_3 = make_solver_3
    rel_abcde = Relation('ABCDE')
    rel_acde = Relation('ACDE')
    rel_ab = Relation('AB')
    rel_ade = Relation('ADE')
    rel_ace = Relation('ACE')
    assert solver_3.is_bcnf(rel_abcde) == False
    assert solver_3.is_bcnf(rel_acde) == False
    assert solver_3.is_bcnf(rel_ab) == True
    assert solver_3.is_bcnf(rel_ade) == True
    assert solver_3.is_bcnf(rel_ace) == True

def test_solver_bcnf_decomp(make_solver_3):
    solver_3 = make_solver_3
    rel_abcde = Relation('ABCDE')
    print(solver_3.find_bcnf_decomp(rel_abcde))
