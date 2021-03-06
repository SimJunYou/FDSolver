import pytest
from fdsolver.classes import FD, FDSet
from fdsolver.io import FDReader, FDWriter

def test_get_fdset():
    fd_abc_de = FD(set('ABC'), set('DE'))
    fd_ad_c = FD(set('AD'), set('C'))
    fd_bcd_ac = FD(set('BCD'), set('AC'))

    comparisonFdSet = FDSet(fd_abc_de, fd_ad_c, fd_bcd_ac)

    reader = FDReader('test_data/test_data_1.txt')
    newFdSet = reader.get_fdset()
    assert newFdSet == comparisonFdSet
    
def test_get_objs():
    fd_abc_de = FD(set('ABC'), set('DE'))
    fd_bcd_ac = FD(set('BCD'), set('AC'))
    rel_ad = set('AD')
    rel_c = set('C')
    
    reader = FDReader('test_data/test_data_2.txt')
    outputList = reader.get_objs()

    assert outputList == [fd_abc_de, rel_ad, fd_bcd_ac, rel_c] 

# No need to test get_solver() since it's just a simple wrapper
# of get_fdset()...

def test_write_objs_to_file(tmpdir):
    p = tmpdir.mkdir('write').join('write_test.txt')
    rel_abc = set('ABC')
    rel_de = set('DE')
    fd_abc_de = FD(rel_abc, rel_de)
    fd_de_abc = FD(rel_de, rel_abc)
    
    writer = FDWriter(str(p))

    proper_output = ''
    for each in (rel_abc, rel_de, fd_abc_de, fd_de_abc):
        proper_output += str(each) + '\n'
        writer.write_obj(each)

    assert p.read_text(None) == proper_output
