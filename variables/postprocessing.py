from os import path

class initialize(object):
    def __init__(self, e):
        self.e = e

        self.s = path.join(self.e.vectors, "s")     # this is the final training observation data
        self.st = path.join(self.e.vectors, "st")   # this is the final modelling input data
        self.tbl_t = path.join(self.e.outputs, "training.txt")
        self.tbl_m = path.join(self.e.outputs, "modelling.txt")