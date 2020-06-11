import re
from os import path
from random import random

class initialize(object):
    def __init__(self, e):
        self.e = e

        ### Temp rasters ####
        self.temps_r = []
        self.temps_v = []
        self.temp0 = path.join(self.e.temp, "temp0")
        self.temp1 = path.join(self.e.temp, "temp1")
        # self.temp2 = path.join(e.temp, "temp2")

    def generate_temps(self, t, p):
        r = str(int(random()*1000000))
        if len(r) < 7:
            z = str(0) * (7-len(r))
        else:
            z = ""
        n = p + z + r
        if t  == "r":
            f = path.join(self.e.temp_r, n)
            self.temps_r.append(f)
            return(f)
        elif t == "v":
            f = path.join(self.e.temp_v, n)
            self.temps_v.append(f)
            return(f)

    def modify_temps(self, n, t, p):
        n = path.basename(n)
        n = re.split('(\d+)',n)
        n = p + n[1]
        if t  == "r":
            f = path.join(self.e.temp_r, n)
            self.temps_r.append(f)
            return(f)
        elif t == "v":
            f = path.join(self.e.temp_v, n)
            self.temps_v.append(f)
            return(f)

    def clear_temps(self, t):
        if t  == "r":
            self.temps_r = []
        elif t == "v":
            self.temps_v = []