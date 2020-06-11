from os import path

class initialize(object):
    def __init__(self, e):
        self.e = e

        self.cmx = path.join(self.e.vectors, "cmx")  # Catchment_Max
        self.drl_c = path.join(self.e.vectors, "drl_c")  # DrainageLine_Clip
        self.lfp_ct = path.join(self.e.vectors, "lfp_ct")  #  lLFP_Clip (temporary)
        self.lfp_c = path.join(self.e.vectors, "lfp_c")  #  lLFP_Clip
        self.fm_vec = path.join(self.e.vectors, "fm_vec")  # FlowlineLine_Clip_Merge
        self.fm_ras = path.join(self.e.rasters, "fm_ras")  # Flowline_ras
        self.fm_ras_d = path.join(self.e.rasters, "fm_ras_d")  # Divide_Flow1
        self.fm_ras_r = path.join(self.e.rasters, "fm_ras_r")  # Reclass_Divi1
        self.fm_ras_c = path.join(self.e.rasters, "fm_ras_c")  # Combine_Recl1
        self.facets = path.join(self.e.vectors, "facets")  # facets