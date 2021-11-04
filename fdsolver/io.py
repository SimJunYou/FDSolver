
class Reader:
    def __init__(self, filepath):
        self.path = filepath

    def read_as_objs(self):
        output = []
        with open(self.path, 'r') as f:
            for eachLine in f.readlines():
                eachLine = eachLine.strip()
                if self._is_line_fd(eachLine):
                    before, after = line.split(' -> ')
                    output.append(FD(eachLine)) 
                elif self._is_line_rel(eachLine):
                    

    def read_as_fdset(self):


    def _is_line_rel(self, line):
        hasBraces = line.startswith('{') and line.endswith('}')
        hasNoDigits = line[1:-1].replace(' ','').replace(',','').isalpha()
        return hasBraces and hasNoDigits
    
    def _is_line_fd(self, line):
        if ' -> ' not in line:
            return False
        before, after = line.split(' -> ')
        return self._is_line_rel(before) and self._is_line_rel(after)
    
    def _line_to_rel(self, line):
        line = line
