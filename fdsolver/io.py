from fdsolver.classes import FD, FDSet
from fdsolver.solver import Solver

class FDReader:
    def __init__(self, filepath):
        self.path = filepath

    def get_objs(self):
        output = []
        with open(self.path, 'r') as f:
            for eachLine in f.readlines():
                eachLine = eachLine.strip()
                if self._is_line_fd(eachLine):
                    lhs, rhs = eachLine.split(' -> ')
                    newFd = FD(self._parse_to_rel(lhs), self._parse_to_rel(rhs))
                    output.append(newFd)
                elif self._is_line_rel(eachLine):
                    newRel = self._parse_to_rel(eachLine)
                    output.append(newRel)
        return output
                    
    def get_fdset(self):
        newFdSet = FDSet()
        with open(self.path, 'r') as f:
            for eachLine in f.readlines():
                eachLine = eachLine.strip()
                if self._is_line_fd(eachLine):
                    lhs, rhs = eachLine.split(' -> ')
                    newFd = FD(self._parse_to_rel(lhs), self._parse_to_rel(rhs))
                    newFdSet.add_step(newFd)
        return newFdSet

    def get_solver(self):
        return Solver(self.get_fdset())
    
    def _parse_to_rel(self, line):
        firstBracket = line.find('{')
        return set(line[firstBracket+1:-1].split(','))

    def _is_line_rel(self, line):
        hasBraces = line.startswith('{') and line.endswith('}')
        hasNoDigits = line[1:-1].replace(' ','').replace(',','').isalpha()
        return hasBraces and hasNoDigits
    
    def _is_line_fd(self, line):
        if ' -> ' not in line:
            return False

        before, after = line.split(' -> ')
        return self._is_line_rel(before) and self._is_line_rel(after)
            

class FDWriter:
    def __init__(self, filepath):
        self.path = filepath

    def write_obj(self, obj):
        if isinstance(obj, set) \
                or isinstance(obj, FD) \
                or isinstance(obj, FDSet):
            with open(self.path, 'a+') as f:
                print(obj, file=f)
        else:
            raise NotImplemented

