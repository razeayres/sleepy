from os import path

class initialize(object):
    def __init__(self, e):
        self.e = e

        self.fac_mf1 = path.join(self.e.rasters, "fac_mf1")  # Plus_FlowAcc1
        # self.fac_area = path.join(self.e.rasters, "fac_area")  # fac_area
        self.As = path.join(self.e.rasters, "As")  # As
        self.b_times = path.join(self.e.rasters, "b_times")  # B_times
        self.b_rad = path.join(self.e.rasters, "b_rad")  # B_rad
        self.b_tan = path.join(self.e.rasters, "b_tan")  # TanB
        self.b_tan_c = path.join(self.e.rasters, "b_tan_c")  # TanBCon
        self.As_b_tan = path.join(self.e.rasters, "As_b_tan")  # AsOverTanB
        self.cti = path.join(self.e.outputs, "cti")  # CTI