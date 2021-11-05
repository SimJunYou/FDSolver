from fdsolver.classes import Relation, FD, FDSet
from random import shuffle 
from typing import List

# Solves based on the set of FDs given to it on initialisation
class Solver:
    def __init__(self, fdSet: FDSet):
        self.fdSet = fdSet

    def implies(self, start: Relation, end: Relation):
        # is 'end' a subset of 'start'+?
        return end in self.closure(start)

    def closure(self, rel: Relation, limit_to: Relation=None):
        # i.e. r{A,B,C} -> [r{A}, r{B}, r{C}]
        if len(rel) == 0:
            return rel
        closure = rel.copy()
        stillValid = True
        while stillValid:
            stillValid = False
            for fd in self.fdSet:
                if fd.before in closure and not fd.after in closure:
                    stillValid = True
                    closure |= fd.after
        return closure 

    def superkeys(self, rel: Relation):
        superkeys = []
        for eachSubset in rel.subsets():
            if len(eachSubset) > 0 and rel in self.closure(eachSubset):
                superkeys.append(eachSubset)
        return superkeys

    def keys(self, rel: Relation):
        superkeys = self.superkeys(rel)
        keys = []
        for i in range(len(superkeys)):
            sub = False
            for j in range(len(superkeys)):
                if (i != j and superkeys[j] in superkeys[i] \
                           and superkeys[i] != superkeys[j]):
                    sub = True
                    break
            if not sub:
                keys.append(superkeys[i])
        return keys

    def prime_attrs(self, rel: Relation):
        keys = self.keys(rel)
        if len(keys) == 0:
            return None

        prime_attrs = keys[0].copy()
        if len(keys) == 1:
            return prime_attrs
        
        for key in keys[1:]:
            prime_attrs |= key
        return prime_attrs

    def is_bcnf(self, rel: Relation):
        for subset in rel.subsets():
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset in cl and subset != cl and cl in rel and cl != rel:
                    return False
        return True

    def interactive_find_bcnf_decomp(self, rel: Relation):
        currentRel = rel.copy()
        while True:
            decomp_list = self._find_bcnf_decomp_helper(currentRel)
            for count, each in enumerate(decomp_list):
                print(f"{count}: {each[0]} - {each[1]}, {each[2]} - {each[3]}")    
            user = input("Decomp next relation (q to stop): ")
            print()
            if user == 'q':
                break
            currentRel = Relation(user)
        return True

    def _find_bcnf_decomp_helper(self, rel: Relation):
        decomp_list = []
        sortedSubsetList = sorted(rel.subsets())
        for subset in sortedSubsetList:
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset in cl and subset != cl and cl in rel and cl != rel:
                    r1 = cl
                    r2 = subset | (rel - cl)
                    decomp_list.append([r1, self.is_bcnf(r1), \
                                        r2, self.is_bcnf(r2)])
        return decomp_list

    def find_bcnf_decomp(self, rel: Relation, randomize=False):
        decomp_list = []
        sortedSubsetList = sorted(rel.subsets())
        if randomize:
            shuffle(sortedSubsetList)
        for subset in sortedSubsetList:
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset in cl and subset != cl and cl in rel and cl != rel:
                    r1 = cl
                    r2 = subset | (rel - cl)
                    decomp_list += self.find_bcnf_decomp(r1, randomize=randomize)
                    decomp_list += self.find_bcnf_decomp(r2, randomize=randomize)
                    break
        if len(decomp_list) == 0:
            return [rel]
        return decomp_list

    def is_lossless_decomp(self, relList: List[Relation], originalRel: Relation):
        if len(relList) <= 1:
            return True
        intersect = relList[0].copy()
        for eachRel in relList[1:]:
            intersect &= eachRel
        superkeys = self.superkeys(originalRel)
        return intersect in superkeys




