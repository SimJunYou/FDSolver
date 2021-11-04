from collections.abc import Iterable

class Relation:
    def __init__(self, elems):
        if not isinstance(elems, Iterable):
            raise TypeError('Relation parameter needs to be Iterable')
        self.elems = set(elems)

    def __len__(self):
        return len(self.elems)

    def __str__(self):
        sortedElems = sorted(list(self.elems))
        return "{" + f"{', '.join(sortedElems)}" + "}"

    class RelationIterator:
        def __init__(self, rel):
            self._len = len(rel)
            self._iter = rel.elems.__iter__()
            self._index = 0

        def __next__(self):
            if self._index < self._len:
                self._index += 1
                return self._iter.__next__()
            raise StopIteration

    def __iter__(self):
        return self.RelationIterator(self)

class FD:
    def __init__(self, before, after):
        if not isinstance(before, Relation) or not isinstance(after, Relation):
            raise TypeError('FD parameters must be Relations')
        self.before = before
        self.after = after

    def decompose(self):
        newFDSet = FDSet()
        for eachAfter in self.after:
            newFD = FD(self.before, Relation(eachAfter))
            newFDSet.add_step(newFD)
        return newFDSet
    
    def __str__(self):
        return str(self.before) + " -> " + str(self.after)

class FDSet:
    def __init__(self):
        self.proof = []
    
    def add_step(self, newFd):
        if not isinstance(newFd, FD):
            raise TypeError('FDSet only accepts an FD as input')
        self.proof.append(newFd)

    def __str__(self):
        outstr = ""
        for eachFd in self.proof:
            outstr += str(eachFd) + "\n"
        return outstr.strip() # remove excess \n
