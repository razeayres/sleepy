import arcpy
from time import sleep

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.run()

    def run(self):
        self.e.load()
        print "Starting CTI processing..."
        arcpy.gp.Plus_sa(self.i.fac_mf, "1", self.i.fac_mf1)
        X_Length = float(arcpy.GetRasterProperties_management(self.i.fac_mf, "CELLSIZEX", "").getOutput(0))
        Y_Length = float(arcpy.GetRasterProperties_management(self.i.fac_mf, "CELLSIZEY", "").getOutput(0))
        # arcpy.gp.Times_sa(str(X_Length), str(Y_Length), self.i.fac_area)
        arcpy.gp.Times_sa(self.i.fac_mf1, str(X_Length * Y_Length), self.i.As)   # this is all for calculating As

        arcpy.gp.Times_sa(self.i.sdg_f, "1.570796", self.i.b_times)
        arcpy.gp.Divide_sa(self.i.b_times, "90", self.i.b_rad)
        arcpy.gp.Tan_sa(self.i.b_rad, self.i.b_tan)
        arcpy.gp.Con_sa(self.i.sdg_f, self.i.b_tan, self.i.b_tan_c, "0.001", "\"Value\" > 0")  # this is all for calculating tanB

        arcpy.gp.Divide_sa(self.i.As, self.i.b_tan_c, self.i.As_b_tan)
        arcpy.gp.Ln_sa(self.i.As_b_tan, self.i.cti)
        print "Ending CTI processing..."