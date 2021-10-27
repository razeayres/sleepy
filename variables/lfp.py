from os import path

class initialize(object):
    def __init__(self, e):
        self.e = e

        self.l_rng = path.join(self.e.rasters, "l_rng.tif")    # RANGE
        self.l_ild = path.join(self.e.rasters, "l_ild")  # ISLANDS
        self.l_ild_n = path.join(self.e.rasters, "l_ild_n")  # IsNull(ISLANDS)
        self.l_ild_n_c = path.join(self.e.rasters, "l_ild_n_c")  # ExtractByMask_sa(IsNull(ISLANDS))
        self.l_fnd = path.join(self.e.rasters, "l_fnd")  # FENCED
        self.l_fill = path.join(self.e.rasters, "l_fill")  # FILLED
        self.l_fdr = path.join(self.e.rasters, "l_fdr")  # FDIR
        self.l_fln = path.join(self.e.rasters, "l_fln")  # FLEN
        self.l_lmx = path.join(self.e.rasters, "l_lmx")  # LENMAX
        self.l_lmx_fln = path.join(self.e.rasters, "l_lmx_fln")  # EqualTo_sa("LENMAX","FLEN")
        self.l_mxp_r = path.join(self.e.rasters, "l_mxp_r")  # MAXPNTS
        self.l_mxp_v = path.join(self.e.vectors, "l_mxp_v")  # SOURCES
        self.l_pth = path.join(self.e.rasters, "l_pth") # CPATHS
        self.l_lfp = path.join(self.e.vectors, "l_lfp") # LongFPs
        self.l_spa = path.join(self.e.vectors, "l_spa")
