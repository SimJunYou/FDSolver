import pytest
from fdsolver.classes import FD, FDSet

def test_fd_decomposition():
    fd_abc_de = FD(set('ABC'), set('DE'))
    fd_abc_d = FD(set('ABC'), set('D'))
    fd_abc_e = FD(set('ABC'), set('E'))
    
    decomposed = fd_abc_de.decompose()
    fdset_2 = FDSet(fd_abc_d, fd_abc_e)
    assert decomposed == fdset_2

def test_fd_union():
    fd_abc_de = FD(set('ABC'), set('DE'))
    fd_abc_d = FD(set('ABC'), set('D'))
    fd_abc_e = FD(set('ABC'), set('E'))
    
    unioned = fd_abc_d | fd_abc_e
    assert unioned == fd_abc_de


