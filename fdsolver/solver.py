from fdsolver.classes import Relation, FD, FDSet
from random import shuffle 
from typing import List

# Solves based on the set of FDs given to it on initialisation
class Solver:
    def __init__(self, fdSet: FDSet):
        self.fdSet = fdSet
        self.completeRel = Relation('')
        for eachFd in fdSet:
            for eachRel in eachFd.before:
                self.completeRel |= eachRel
            for eachRel in eachFd.after:
                self.completeRel |= eachRel

    def implies(self, start: Relation, end: Relation):
        # is 'end' a subset of 'start'+?
        return end in self.closure(start)

    def closure(self, rel: Relation = None, limit_to:Relation = None):
        # i.e. r{A,B,C} -> [r{A}, r{B}, r{C}]
        if rel == None:
            rel = self.completeRel.copy()
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

    def superkeys(self, rel:Relation = None):
        if rel == None:
            rel = self.completeRel.copy()
        superkeys = []
        for eachSubset in rel.subsets():
            if len(eachSubset) > 0 and rel in self.closure(eachSubset):
                superkeys.append(eachSubset)
        return superkeys

    def keys(self, rel:Relation = None):
        if rel == None:
            rel = self.completeRel.copy()
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

    def prime_attrs(self, rel:Relation = None):
        if rel == None:
            rel = self.completeRel.copy()
        keys = self.keys(rel)
        if len(keys) == 0:
            return None

        prime_attrs = keys[0].copy()
        if len(keys) == 1:
            return prime_attrs
        
        for key in keys[1:]:
            prime_attrs |= key
        return prime_attrs

    def is_bcnf(self, rel:Relation = None):
        if rel == None:
            rel = self.completeRel.copy()
        for subset in rel.subsets():
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset in cl and subset != cl and cl in rel and cl != rel:
                    return False
        return True

    def interactive_find_bcnf_decomp(self, rel:Relation = None):
        if rel == None:
            rel = self.completeRel.copy()
        decomp_queue = [rel]
        final_decomp = []
        while True:
            print("Current queue:", ", ".join(map(str, decomp_queue)))
            print("Current item   ^\n")
            currentRel = decomp_queue.pop(0)
            decomp_list = self._find_bcnf_decomp_helper(currentRel)
            print("All available decompositions:")
            for count, each in enumerate(decomp_list):
                print(f"{count+1}: {each[0]} - {each[1]}, {each[2]} - {each[3]} ",end='')
                print(f"(Lossless: {each[4]})")
            user = input("Choose pair to add to queue (q to stop): ")
            print()
            if user == 'q' or not user.isdigit():
                break

            # iterate through each set's [0] and [2]
            allBCNF = True
            for r in decomp_list[int(user)-1][:3:2]:
                if not self.is_bcnf(r):
                    allBCNF = False
                    decomp_queue.append(r)
                else:
                    final_decomp.append(r)
            if allBCNF:
                print("All done! Your final decomposition:", ', '.join(map(str, final_decomp)))
                return

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
                                        r2, self.is_bcnf(r2), \
                                        self.is_lossless_decomp(r1,r2)])
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

    def is_lossless_decomp(self, rel1:Relation, rel2:Relation, originalRel:Relation = None):
        if originalRel == None:
            originalRel = self.completeRel.copy()
        intersect = rel1 & rel2
        closure = self.closure(intersect, limit_to=originalRel)
        return any([rel in closure for rel in (rel1, rel2)])



