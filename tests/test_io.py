import pytest
from fdsolver.classes import Relation, FD, FDSet
from fdsolver.io import FDReader, FDWriter

def test_read_file_as_fdset():
    fd_abc_de = FD(Relation('ABC'), Relation('DE'))
    fd_ad_c = FD(Relation('AD'), Relation('C'))
    fd_bcd_ac = FD(Relation('BCD'), Relation('AC'))

    comparisonFdSet = FDSet(fd_abc_de, fd_ad_c, fd_bcd_ac)

    reader = FDReader('test_data/test_data_1.txt')
    newFdSet = reader.read_as_fdset()
    assert newFdSet == comparisonFdSet
    
def test_read_file_as_objs():
    fd_abc_de = FD(Relation('ABC'), Relation('DE'))
    fd_bcd_ac = FD(Relation('BCD'), Relation('AC'))
    rel_ad = Relation('AD')
    rel_c = Relation('C')
    
    reader = FDReader('test_data/test_data_2.txt')
    outputList = reader.read_as_objs()

    assert outputList == [fd_abc_de, rel_ad, fd_bcd_ac, rel_c] 

def test_write_objs_to_file(tmpdir):
    p = tmpdir.mkdir('write').join('write_test.txt')
    rel_abc = Relation('ABC')
    rel_de = Relation('DE')
    fd_abc_de = FD(rel_abc, rel_de)
    fd_de_abc = FD(rel_de, rel_abc)
    
    writer = FDWriter(str(p))

    proper_output = ''
    for each in (rel_abc, rel_de, fd_abc_de, fd_de_abc):
        proper_output += str(each) + '\n'
        writer.write_obj(each)

    assert p.read_text(None) == proper_output
