from classes import *

class FDGraph:
    def __init__(self, fdSet):
        if not isinstance(fdSet, FDSet):
            raise TypeError("FDGraph must be given a FDSet")

