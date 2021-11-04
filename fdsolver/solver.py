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

    def closure(self, rel: Relation, no_trivial=False, limit_to: Relation=None):
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
        final_closure = closure
        if no_trivial:
            final_closure -= rel
        if limit_to:
            final_closure &= limit_to
        return final_closure

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

    # most definitely not working
    # apparently finding lossless decomp to bcnf is NP-Complete
    def find_satisfactory_bcnf_decomp(self, rel: Relation):
        # This is bogo-find :)
        keys = self.keys(rel)
        while True:
            latest_decomp = self.find_bcnf_decomp(rel, randomize=True)
            for eachKey in keys:
                if eachKey in latest_decomp:
                    pass
            if all([eachKey not in latest_decomp]):
                latest_decomp.append(keys[0])
            if self.is_lossless_decomp(latest_decomp):
                break
        return latest_decomp

    def find_bcnf_decomp(self, rel: Relation, randomize=False):
        decomp_list = []
        sortedSubsetList = sorted(rel.subsets(), reverse=True)

        # Shuffle the sorted subset list randomly
        # The order of subsets affects the decomposition found
        if randomize:
            shuffle(sortedSubsetList)

        for subset in sortedSubsetList:
            if len(subset) > 0:
                cl = self.closure(subset, no_trivial=True, limit_to=rel) & rel
                if len(cl) > 0:
                    decomp_list += self.find_bcnf_decomp(subset, randomize=randomize)
                    decomp_list += self.find_bcnf_decomp(cl - subset, randomize=randomize)
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




