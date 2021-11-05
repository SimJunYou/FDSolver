from fdsolver.classes import Relation, FD, FDSet
from random import shuffle 
from typing import List

# Solves based on the set of FDs given to it on initialisation
class Solver:
    '''
    Contains all solving functions to be used on a FD set.

    Constructors:
    __init__()

    Operators:
    __str__, __repr__
    '''

    def __init__(self, fdSet):
        '''
        Initializes the solver based on a given FD set.
        
        :param fdSet: All solver solutions will be based on this set (unless specified otherwise).
        :returns: None
        '''
        
        self.fdSet = fdSet
        self.completeRel = Relation('')
        for eachFd in fdSet:
            for eachRel in eachFd.before:
                self.completeRel |= eachRel
            for eachRel in eachFd.after:
                self.completeRel |= eachRel

    def __str__(self):
        return str(self.fdSet)
    
    def __repr__(self):
        return self.fdSet

    def implies(self, start, end):
        '''
        Returns whether `start` implies `end`, via the FD set given to the solver.

        :param start: The source relation.
        :param end: The target relation.
        :returns: A boolean.
        '''
        
        return end in self.closure(start)

    def closure(self, rel=None, limit_to=None):
        '''
        Returns the closure of `rel` on the solver's FD set in one relation.
        Can be limited to a set of elements (specified together in one relation).
        Will include 'trivial' relations in the output!
        
        :param rel: The relation to find the closure of.
        :param limit_to: The relation to limit the closure's relations to.
        :returns: The relation representing the closure.
        '''
        
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

    def superkeys(self, rel=None):
        '''
        Returns the superkeys of the given relation on the solver's FD set.

        :param rel: The relation to find the superkeys of.
        :returns: A list of relations representing each of the superkeys.
        '''
        
        if rel == None:
            rel = self.completeRel.copy()
        superkeys = []
        for eachSubset in rel.subsets():
            if len(eachSubset) > 0 and rel in self.closure(eachSubset):
                superkeys.append(eachSubset)
        return superkeys

    def keys(self, rel=None):
        '''
        Returns the keys of the given relation on the solver's FD set.

        :param rel: The relation to find the keys of.
        :returns: A list of relations representing each of the keys.
        '''
        
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

    def prime_attrs(self, rel=None):
        '''
        Returns the prime attributes of the given relatio non the solver's FD set.

        :param rel: The relation to find the prime attributes of.
        :returns: A relation with each of the prime attributes.
        '''
        
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

    def is_bcnf(self, rel=None):
        '''
        Checks whether a relation is in BCNF. 
        Does so by checking whether any subset fulfils the following condition:
        >> subset is strict subset of subset's closure
        >> AND subset's closure is strict subset of original relation
        If so, then the relation is NOT in BCNF.

        :param rel: The relation to check.
        :returns: A boolean.
        '''
        
        if rel == None:
            rel = self.completeRel.copy()
        for subset in rel.subsets():
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset in cl and subset != cl and cl in rel and cl != rel:
                    return False
        return True

    def interactive_find_bcnf_decomp(self, rel=None):
        '''
        Creates an interactive menu to assist in finding ideal BCNF decompositions.
        Lets users choose which decomposition of the current relation to use.
        Prints the list of chosen decompositions at the end.
        May be buggy.

        :params rel: The relation to be decomposed.
        :returns: None (output is printed).
        '''
        
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

    def _find_bcnf_decomp_helper(self, rel):
        '''
        Helper function for the interactive BCNF decomposer.
        Similar to find_bcnf_decomp, but puts the decompositions in an array structure
        together with some more useful information instead of recursing further down.

        :param rel: The relation to be decomposed.
        :returns: The array structure with the decomposition and more info.
        '''
        
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

    def find_bcnf_decomp(self, rel, randomize=False):
        '''
        Finds the BCNF decomposition of any relation on the solver's FD set.
        Since the optimal decomposition is unknown, there is a `randomize` param
        to shuffle the subsets and get a different decomposition as output.

        :param randomize: Flag to trigger randomization.
        :returns: A list of relations which will be the BCNF decomposition.
        '''

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

    def is_lossless_decomp(self, rel1, rel2, originalRel = None):
        '''
        Checks if two relations that resulted from a BCNF decomposition can be
        losslessly joined.

        :param rel1: The first decomposed relation.
        :param rel2: The second decomposed relation.
        :returns: Whether it is a lossless decomposition.
        '''

        if originalRel == None:
            originalRel = self.completeRel.copy()
        intersect = rel1 & rel2
        closure = self.closure(intersect, limit_to=originalRel)
        return rel1 in closure or rel2 in closure



