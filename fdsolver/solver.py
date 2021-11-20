from fdsolver.classes import FD, FDSet
from itertools import chain, combinations
from random import shuffle 

# Solves based on the set of FDs given to it on initialisation
class Solver:
    '''
    Contains all solving functions. They may or may not be dependent on the FD Set.

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
        self.completeRel = set()
        for eachFd in fdSet:
            for eachRel in eachFd.lhs:
                self.completeRel |= set(eachRel)
            for eachRel in eachFd.rhs:
                self.completeRel |= set(eachRel)

    def __str__(self):
        return str(self.fdSet)
    
    def __repr__(self):
        return self.fdSet

    def subsets(self, rel):
        '''
        Returns all the subsets of the given set in a list.
        
        :param rel: The set to find the subsets of.
        :returns: A list of sets.
        '''
        lst = [set(item) for item in rel]
        allSubsets = list(chain.from_iterable( \
                            combinations(lst, r) for r in range(len(lst)+1)))
        unionedSubsets = []
        for eachSubset in allSubsets:
            if len(eachSubset) == 0:
                continue
            currRel = set(eachSubset[0])  # Make a copy
            for eachRel in eachSubset[1:]:
                currRel |= set(eachRel)
            unionedSubsets.append(currRel)
        return unionedSubsets

    def implies(self, fd):
        '''
        Returns whether a FD is valid via the FD set given to the solver.

        :param fd: The FD to be checked.
        :returns: A boolean.
        '''
        
        return fd.rhs.issubset(self.closure(fd.lhs))

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
            rel = set(self.completeRel)  # Make a copy
        if len(rel) == 0:
            return rel
        closure = set(rel)  # Make a copy again... just to be safe
        stillValid = True
        while stillValid:
            stillValid = False
            for fd in self.fdSet:
                if fd.lhs.issubset(closure) and not fd.rhs.issubset(closure):
                    stillValid = True
                    closure |= fd.rhs
        return closure 

    def superkeys(self, rel=None):
        '''
        Returns the superkeys of the given relation on the solver's FD set.

        :param rel: The relation to find the superkeys of.
        :returns: A list of relations representing each of the superkeys.
        '''
        
        if rel == None:
            rel = set(self.completeRel)
        superkeys = []
        for eachSubset in self.subsets(rel):
            if len(eachSubset) > 0 and rel.issubset(self.closure(eachSubset)):
                superkeys.append(eachSubset)
        return superkeys

    def keys(self, rel=None):
        '''
        Returns the keys of the given relation on the solver's FD set.

        :param rel: The relation to find the keys of.
        :returns: A list of relations representing each of the keys.
        '''
        
        if rel == None:
            rel = set(self.completeRel)
        superkeys = self.superkeys(rel)
        keys = []
        for i in range(len(superkeys)):
            sub = False
            for j in range(len(superkeys)):
                if (i != j and superkeys[j].issubset(superkeys[i]) \
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
            rel = set(self.completeRel)
        keys = self.keys(rel)
        if len(keys) == 0:
            return None

        prime_attrs = set(keys[0])
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
            rel = set(self.completeRel)
        for subset in self.subsets(rel):
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset.issubset(cl) and subset != cl and cl.issubset(rel) and cl != rel:
                    return False
        return True

    def interactive_find_bcnf_decomp(self, rel=None):
        '''
        Creates an interactive menu to assist in finding ideal BCNF decompositions.
        Lets users choose which decomposition of the current relation to use.
        Prints the list of chosen decompositions at the end.

        :params rel: The relation to be decomposed.
        :returns: None (output is printed).
        '''
        
        if rel == None:
            rel = set(self.completeRel)
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
                print(f"(Dependency-Preserving: {each[4]})")
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
            if allBCNF and len(decomp_queue) == 0:
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
        sortedSubsetList = sorted(self.subsets(rel))
        for subset in sortedSubsetList:
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset.issubset(cl) and subset != cl and cl.issubset(rel) and cl != rel:
                    r1 = cl
                    r2 = subset | (rel - cl)
                    decomp_list.append([r1, self.is_bcnf(r1), \
                                        r2, self.is_bcnf(r2), \
                                        self.is_dependency_preserving(r1,r2)])
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
        sortedSubsetList = sorted(self.subsets(rel))
        if randomize:
            shuffle(sortedSubsetList)
        for subset in sortedSubsetList:
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset.issubset(cl) and subset != cl and cl.issubset(rel) and cl != rel:
                    r1 = cl
                    r2 = subset | (rel - cl)
                    decomp_list += self.find_bcnf_decomp(r1, randomize=randomize)
                    decomp_list += self.find_bcnf_decomp(r2, randomize=randomize)
                    break
        if len(decomp_list) == 0:
            return [rel]
        return decomp_list

    def is_dependency_preserving(self, rel1, rel2):
        '''
        Checks whether the decomposition of two relations (decomposed from one parent relation)
        is dependency preserving or not.

        :param rel1: The first relation in the decomposition.
        :param rel2: The second relation in the decomposition.
        :returns: A boolean value.
        '''

        solver1 = Solver(self.fdSet.get_sub_fdset(rel1))
        solver2 = Solver(self.fdSet.get_sub_fdset(rel2))
        
        for eachFd in self.fdSet:
            if not (solver1.implies(eachFd) or solver2.implies(eachFd)):
                return False
        return True

    def is_lossless_decomp(self, rel1, rel2, originalRel=None):
        '''
        Checks if two relations can be losslessly joined under the current solver's FD set.

        :param rel1: The first relation.
        :param rel2: The second relation.
        :returns: Whether it is a lossless decomposition.
        '''

        if originalRel == None:
            originalRel = set(self.completeRel)
        intersect = rel1 & rel2
        closure = self.closure(intersect, limit_to=originalRel)
        return rel1.issubset(closure) or rel2.issubset(closure)

    def is_3nf(self, rel):
        '''
        Checks whether a relation is in BCNF. 
        Does so by checking whether any subset fulfils the following condition:
        >> subset is strict subset of subset's closure
        >> AND subset's closure is strict subset of original relation
        >> AND subset's closure - subset does not include any prime attributes
        If so, then the relation is NOT in BCNF.

        :param rel: The relation to check.
        :returns: A boolean.
        '''
        
        if rel == None:
            rel = set(self.completeRel)
        for subset in self.subsets(rel):
            if len(subset) > 0:
                cl = self.closure(subset) & rel
                if subset.issubset(cl) and subset != cl and cl.issubset(rel) and cl != rel:
                    return (cl - subset) in self.prime_attrs()
        return True

    def find_minimal_basis(self):
        # Step 1: Non-trivialize and decompose
        fullyDecomposed = []
        for eachFd in self.fdSet:  
            eachFd = eachFd.untrivialize()
            decomposed = eachFd.decompose()
            for eachDecomp in decomposed:
                fullyDecomposed.append(eachDecomp)
       
        # Step 2: Remove redundant attributes on LHS of each FD
        newFdSet = []
        for eachFd in fullyDecomposed:
            newBefore = set()
            for eachRel in eachFd.lhs:
                eachRel = set(eachRel)
                if not eachFd.rhs.issubset(self.closure(eachFd.lhs - eachRel)):
                    newBefore |= eachRel
            eachFd.lhs = newBefore
            if eachFd not in newFdSet:
                newFdSet.append(eachFd)
        
        # Step 3: Remove redundant FDs
        changesRemain = True
        while changesRemain:
            changesRemain = False
            index = 0
            while index < len(newFdSet):
                eachFd = newFdSet[index]
                # Make a solver that excludes only the current FD
                # If the solver can infer the current FD, then it is redundant
                fdSetWithoutFd = [fd for fd in newFdSet if fd != eachFd]
                temp_solver = Solver(FDSet(*fdSetWithoutFd))
                if not temp_solver.implies(eachFd):
                    index += 1
                else:
                    changesRemain = True
                    newFdSet.pop(index)

        return FDSet(*newFdSet)


        


