import pytest
from fdsolver.classes import Relation, FD, FDSet
from fdsolver.solver import Solver
from fdsolver.io import FDReader
from tests.fixtures import make_solver_1, make_solver_2, make_solver_3, make_solver_4

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
    assert solver_2.closure(rel_b) == Relation('B')
    assert solver_2.closure(Relation('AC')) == Relation('ABCDE')


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


@pytest.mark.parametrize('execution_count', range(10))
def test_solver_bcnf_decomp(make_solver_3, execution_count):
    solver_3 = make_solver_3
    rel_abcde = Relation('ABCDE')
    bcnf_list = solver_3.find_bcnf_decomp(rel_abcde, randomize=True)
    for each in bcnf_list:
        assert solver_3.is_bcnf(each) == True

'''
def test_interactive_bcnf_decomp(make_solver_3):
    solver_3 = make_solver_3
    rel_abcde = Relation('ABCDE')
    assert solver_3.interactive_find_bcnf_decomp(rel_abcde)
'''

def test_solver_is_lossless_decomp(make_solver_3):
    solver_3 = make_solver_3
    rel_abcde = Relation('ABCDE')
    assert not solver_3.is_lossless_decomp(Relation('ACE'), Relation('BD'))
    assert solver_3.is_lossless_decomp(Relation('ACED'), Relation('ACEB'))

def test_solver_is_3nf(make_solver_4):
    solver_4 = make_solver_4
    rel_abcde = Relation('ABCDE')
    rel_acde = Relation('ACDE')
    rel_bde = Relation('BDE')
    rel_cde = Relation('CDE')
    rel_bcd = Relation('BCD')
    assert solver_4.is_bcnf(rel_abcde) == False
    assert solver_4.is_bcnf(rel_acde) == False
    assert solver_4.is_bcnf(rel_bde) == True
    assert solver_4.is_bcnf(rel_cde) == True
    assert solver_4.is_bcnf(rel_bcd) == True

def test_solver_find_minimal_basis(make_solver_4):
    solver_4 = make_solver_4
    fd_bd_e = FD(Relation('BD'), Relation('E'))
    fd_ce_b = FD(Relation('CE'), Relation('B'))
    fd_ce_d = FD(Relation('CE'), Relation('D'))
    fd_cd_e = FD(Relation('CD'), Relation('E'))

    minbasis = solver_4.find_minimal_basis()
    assert fd_bd_e in minbasis
    assert fd_ce_b in minbasis 
    assert fd_ce_d in minbasis 
    assert fd_cd_e in minbasis
    assert len(minbasis) == 4


