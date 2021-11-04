from fdsolver.classes import Relation, FD, FDSet
from typing import List

# Solves based on the set of FDs given to it on initialisation
class Solver:
    def __init__(self, fdSet: FDSet):
        self.fdSet = fdSet

    def implies(self, start: Relation, end: Relation):
        # is 'end' a subset of 'start'+?
        return end in self.closure(start)

    def closure(self, rel: Relation, no_trivial=False):
        # i.e. r{A,B,C} -> [r{A}, r{B}, r{C}]
        closure = rel.copy()
        stillValid = True
        while stillValid:
            stillValid = False
            for fd in self.fdSet:
                if fd.before in closure and not fd.after in closure:
                    stillValid = True
                    closure |= fd.after
        if no_trivial:
            return closure - rel
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

    def find_bcnf_decomp(self, rel: Relation):
        decomp_list = []
        for subset in rel.subsets():
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset in cl and subset != cl and cl in rel and cl != rel:
                    decomp_list.append(self.find_bcnf_decomp(subset))
                    decomp_list.append(self.find_bcnf_decomp(cl - subset))
                    break
        if len(decomp_list) == 0:
            return rel
        return decomp_list


    def is_lossless_decomp(self, relList: List[Relation]):
        if len(relList) <= 1:
            return True
        rel = relList[0].copy()
        for eachRel in relList[1:]:
            rel &= eachRel
        closure = self.closure(rel)
        
        return any([(eachRel in closure) for eachRel in relList])




