import pytest
from fdsolver.classes import FD, FDSet
from fdsolver.solver import Solver
from fdsolver.io import FDReader
from tests.fixtures import make_solver_1, make_solver_2, make_solver_3, make_solver_4

def test_rel_generate_subsets(make_solver_1):
    # Subset finding actually doesn't require the solver's FD
    # but it needs the solver object anyways so...
    solver_1 = make_solver_1
    rel_abc = set('ABC') 
    subsets = solver_1.subsets(rel_abc)
    assert set('A') in subsets
    assert set('B') in subsets
    assert set('C') in subsets
    assert set('AB') in subsets
    assert set('AC') in subsets
    assert set('BC') in subsets
    assert set('ABC') in subsets
    assert len(subsets) == 7

def test_solver_closure(make_solver_1, make_solver_2):
    solver_1 = make_solver_1

    assert solver_1.closure(set('A')) == set('ABCDE')
    assert solver_1.closure(set('B')) == set('BCDE')
    assert solver_1.closure(set('C')) == set('CDE')
    assert solver_1.closure(set('D')) == set('DE')
    assert solver_1.closure(set('E')) == set('E')

    solver_2 = make_solver_2

    assert solver_2.closure(set('A')) == set('AB')
    assert solver_2.closure(set('B')) == set('B')
    assert solver_2.closure(set('AC')) == set('ABCDE')

def test_solver_superkeys(make_solver_2):
    solver_2 = make_solver_2
    sol2_sk = solver_2.superkeys(set('ABCDE'))
    assert set('ABCDE') in sol2_sk
    assert set('ABCD') in sol2_sk
    assert set('ABCE') in sol2_sk
    assert set('ABC') in sol2_sk
    assert set('ACDE') in sol2_sk
    assert set('ACD') in sol2_sk
    assert set('ACE') in sol2_sk
    assert set('AC') in sol2_sk
    assert len(sol2_sk) == 8

def test_solver_keys(make_solver_2):
    solver_2 = make_solver_2
    sol2_keys = solver_2.keys(set('ABCDE'))
    assert sol2_keys[0] == set('AC')
    assert len(sol2_keys) == 1

def test_solver_prime_attrs(make_solver_2):
    solver_2 = make_solver_2
    assert solver_2.prime_attrs(set('ABCDE')) == set('AC')
    
def test_solver_is_bcnf(make_solver_3):
    solver_3 = make_solver_3
    assert solver_3.is_bcnf(set('ABCDE')) == False
    assert solver_3.is_bcnf(set('ACDE')) == False
    assert solver_3.is_bcnf(set('AB')) == True
    assert solver_3.is_bcnf(set('ADE')) == True
    assert solver_3.is_bcnf(set('ACE')) == True

@pytest.mark.parametrize('execution_count', range(10))
def test_solver_bcnf_decomp(make_solver_3, execution_count):
    solver_3 = make_solver_3
    bcnf_list = solver_3.find_bcnf_decomp(set('ABCDE'), randomize=True)
    for each in bcnf_list:
        assert solver_3.is_bcnf(each) == True

def test_solver_is_lossless_decomp(make_solver_3):
    solver_3 = make_solver_3
    assert not solver_3.is_lossless_decomp(set('ACE'), set('BD'))
    assert solver_3.is_lossless_decomp(set('ACED'), set('ACEB'))

def test_solver_is_3nf(make_solver_4):
    solver_4 = make_solver_4
    assert solver_4.is_bcnf(set('ABCDE')) == False
    assert solver_4.is_bcnf(set('ACDE')) == False
    assert solver_4.is_bcnf(set('BDE')) == True
    assert solver_4.is_bcnf(set('CDE')) == True
    assert solver_4.is_bcnf(set('BCD')) == True

def test_solver_find_minimal_basis(make_solver_4):
    solver_4 = make_solver_4
    minbasis = solver_4.find_minimal_basis()

    redundancy_exists = False
    for eachFd in minbasis:
        filtered_minbasis = [each for each in minbasis if each != eachFd]
        temp_solver = Solver(FDSet(*filtered_minbasis))
        if temp_solver.implies(eachFd):
            redundancy_exists = True
            break

    assert not redundancy_exists

'''
def test_interactive_bcnf_decomp(make_solver_3):
    solver_3 = make_solver_3
    rel_abcde = set('ABCDE')
    solver_3.interactive_find_bcnf_decomp(rel_abcde)
    assert True
'''
