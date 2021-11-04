from collections.abc import Iterable
from itertools import chain, combinations

class Relation:
    def __init__(self, elems, name='r', fileInput=None):
        if fileInput and isinstance(fileInput, str):
            firstBracket = fileInput.find('{')
            self.elems = set(fileInput[firstBracket+1:-1].split(','))
            if firstBracket != 0:
                self.name = fileInput[:firstBracket+1]
            else:
                self.name = name
            return
        
        if not isinstance(elems, Iterable):
            raise TypeError('Relation parameter needs to be Iterable')
        if not isinstance(name, str):
            raise TypeError('Relation name needs to be String')
        self.elems = set(elems)
        self.name = name

    def __len__(self):
        return len(self.elems)

    def __str__(self):
        sortedElems = sorted(list(self.elems))
        return self.name + "{" + f"{','.join(sortedElems)}" + "}"
    
    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Relation(self.elems)
    
    def deepcopy(self):
        newSet = {}
        for each in self.elems:
            newSet.add(each.copy())
        return Relation(newSet)

    def subsets(self):
        lst = [rel for rel in self]
        allSubsets = list(chain.from_iterable( \
                            combinations(lst, r) for r in range(len(lst)+1)))
        unionedSubsets = []
        for eachSubset in allSubsets:
            if len(eachSubset) == 0:
                continue
            currRel = eachSubset[0].copy()
            for eachRel in eachSubset[1:]:
                currRel |= eachRel
            unionedSubsets.append(currRel)
        return unionedSubsets

    class RelationIterator:
        def __init__(self, rel):
            self._len = len(rel)
            self._iter = rel.elems.__iter__()
            self._index = 0

        def __next__(self):
            if self._index < self._len:
                self._index += 1
                return Relation([self._iter.__next__()])
            raise StopIteration

    def __iter__(self):
        return self.RelationIterator(self)

    # Commandeering the 'in' keyword as a subset operator
    # i.e. R1 in R2 --> is R1 a subset of R2?
    def __contains__(self, other):
        if not isinstance(other, Relation):
            return NotImplemented
        return other.elems.issubset(self.elems)

    # == and != operator
    def __eq__(self, other):
        return self.elems == other

    # | and |= operators (union)
    def __or__(self, other):
        if not isinstance(other, Relation):
            return NotImplemented
        new = self.elems | other.elems
        return Relation(new)
    def __ior__(self, other):
        self.elems |= other.elems
        return self
    
    # & and &= operators (intersect)
    def __and__(self, other):
        if not isinstance(other, Relation):
            return NotImplemented
        new = self.elems & other.elems
        return Relation(new)
    def __iand__(self, other):
        self.elems &= other.elems
        return self

    # - and -= operators (difference)
    def __sub__(self, other):
        if not isinstance(other, Relation):
            return NotImplemented
        new = self.elems - other.elems
        return Relation(new)
    def __isub__(self, other):
        self.elems -= other.elems
        return self


class FD:
    def __init__(self, bef, aft, fileInput=None):
        if fileInput and isinstance(fileInput, str):
            before, after = fileInput.split(' -> ')
            self.before = Relation(None, fileInput=before)
            self.after = Relation(None, fileInput=after)
        elif bef and aft:
            if not isinstance(bef, Relation) or not isinstance(aft, Relation):
                raise TypeError('FD instancing tuple must contain Relations')
            else:
                self.before = bef
                self.after = aft
                return
        else:
            raise TypeError('No valid arguments to FD constructor')

    def decompose(self):
        newFDSet = FDSet()
        for eachAfter in self.after:
            newFD = FD(self.before, eachAfter)
            newFDSet.add_step(newFD)
        return newFDSet
    
    def augment(self, new):
        if not isinstance(new, Relation):
            raise NotImplemented
        self.before |= new
        self.after |= new

    def unaugment(self):
        # i.e. {A,C} -> {A,D} becomes {C} -> {D}
        intersection = self.before & self.after
        self.before -=  intersection
        self.after -= intersection

    def __str__(self):
        return str(self.before) + " -> " + str(self.after)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, FD):
            raise NotImplemented
        return self.before == other.before and self.after == other.after

    # Rule of Union mapped to the | and |= operator
    def __or__(self, other):
        if not isinstance(other, FD):
            raise NotImplemented
        if self.before == other.before:
            return FD(self.before, self.after | other.after)
    
    def __ior__(self, other):
        if not isinstance(other, FD):
            raise NotImplemented
        if self.before == other.before:
            self.after |= other.after

class FDSet:
    def __init__(self, *args):
        self.proof = [*args]

    def add_step(self, newFd):
        if not isinstance(newFd, FD):
            raise NotImplemented 
        self.proof.append(newFd)

    def __str__(self):
        outstr = ""
        for eachFd in self.proof:
            outstr += str(eachFd) + "\n"
        return outstr.strip() # remove excess \n

    def __len__(self):
        return len(self.proof)

    def __getitem__(self, key):
        return self.proof[key]

    def __setitem__(self, key, newFd):
        if not isinstance(newFd, FD):
            raise TypeError('FDSet only accepts an FD as input')
        self.proof[key] = newFd

    # Iterator subclass to allow for iteration
    class FDSetIterator:
        def __init__(self, fdSet):
            self._len = len(fdSet)
            self._iter = fdSet.proof.__iter__()
            self._index = 0

        def __next__(self):
            if self._index < self._len:
                self._index += 1
                return self._iter.__next__()
            raise StopIteration

    def __iter__(self):
        return self.FDSetIterator(self)

    # Implementing 'in' keyword
    def __contains__(self, item):
        return item in self.proof

    def __eq__(self, other):
        if not isinstance(other, FDSet):
            raise TypeError('Cannot compare FDSet to non-FDSet object')
        ans = True
        for eachFd in self:
            if eachFd not in other:
                ans = False
                break
        return ans and len(self) == len(other)

