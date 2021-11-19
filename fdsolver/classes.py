from collections.abc import Iterable

class FD:
    '''
    Abstract representation of a functional dependency.
    Uses the Relation class defined earlier to express both sides of the FD.
    Not much use by itself; commonly used to construct FDSets.

    Constructors:
    __init__()

    Operators:
    __str__, __repr__
    __eq__
    __or__, __ior__

    Methods:
    decompose()
    augment(new), unaugment()

    Properties:
    lhs, rhs (i.e. lhs -> rhs)
    '''

    def __init__(self, lhs, rhs, fileInput=None):
        self.lhs = lhs
        self.rhs = rhs

    def decompose(self):
        newFDSet = FDSet()
        for eachAfter in self.rhs:
            newFD = FD(self.lhs, set(eachAfter))
            newFDSet.add_step(newFD)
        return newFDSet
    
    def augment(self, new):
        if not isinstance(new, Relation):
            raise NotImplemented
        self.lhs |= new
        self.rhs |= new

    def unaugment(self):
        # i.e. {A,C} -> {A,D} becomes {A,C} -> {D}
        intersection = self.lhs & self.rhs
        newLhs, newRhs = set(self.lhs), set(self.rhs)
        newRhs -= intersection
        return FD(self.lhs, newRhs)

    def __str__(self):
        return str(self.lhs) + " -> " + str(self.rhs)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, FD):
            raise NotImplemented
        return self.lhs == other.lhs and self.rhs == other.rhs

    # Rule of Union mapped to the | and |= operator
    def __or__(self, other):
        if not isinstance(other, FD):
            raise NotImplemented
        if self.lhs == other.lhs:
            return FD(self.lhs, self.rhs | other.rhs)
    
    def __ior__(self, other):
        if not isinstance(other, FD):
            raise NotImplemented
        if self.lhs == other.lhs:
            self.rhs |= other.rhs


class FDSet:
    '''
    Abstract representation of a set of functional dependencies.
    Uses the FD class defined earlier.
    Can iterate and get/set using indexing.
    Mimicks a set, in that no duplicates exist.
    Ordered, but there's no point to ordering the FDs anyways.


    Constructors:
    __init__()

    Operators:
    __str__, __repr__
    __len__
    __getitem__, __setitem__
    __iter__, __contains__
    __eq__

    Methods:
    add_step()

    Properties:
    proof
    '''

    def __init__(self, *args):
        self.proof = []
        for eachFd in args:
            self.add_step(eachFd)

    def add_step(self, newFd):
        if not isinstance(newFd, FD):
            raise NotImplemented
        if newFd not in self.proof:
            self.proof.append(newFd)

    def __str__(self):
        outstr = ""
        for eachFd in self.proof:
            outstr += str(eachFd) + "\n"
        return outstr.strip() # remove excess \n

    def __repr__(self):
        return self.__str__()

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

