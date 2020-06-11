from os import path

class initialize(object):
    def __init__(self, e):
        self.e = e

        self.fill = path.join(self.e.rasters, "fill")    # fil2
        self.fdr = path.join(self.e.rasters, "fdr")  # fdr
        self.fac = path.join(self.e.rasters, "fac")  # fac
        self.std = path.join(self.e.rasters, "std")  # str
        self.sts = path.join(self.e.rasters, "sts")  # strlnk
        self.drl = path.join(self.e.vectors, "drl")  # DrainageLine
        self.cat = path.join(self.e.rasters, "cat")  # cat
        self.catchment = path.join(self.e.vectors, "catchment")  # catchment
        self.lfp = path.join(self.e.vectors, "lfp")  # LongestFlowPathCat