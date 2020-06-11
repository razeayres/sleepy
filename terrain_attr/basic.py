import arcpy

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.run()

    def run(self):
        self.e.load()
        arcpy.gp.IsNull_sa(self.i.fm_ras, self.i.std_null)
        # arcpy.gp.MakeRasterLayer(self.i.std_null, "std_null")
        arcpy.gp.SetNull_sa(self.i.std_null, self.i.std_null, self.i.mask, """"VALUE" = 0""")
        arcpy.gp.ExtractByMask_sa(self.i.fdr, self.i.mask, self.i.fdr_mf)
        arcpy.gp.ExtractByMask_sa(self.i.fill, self.i.mask, self.i.fill_mf)
        arcpy.gp.ExtractByMask_sa(self.i.fac, self.i.mask, self.i.fac_mf)
        arcpy.BuildRasterAttributeTable_management(self.i.fac_mf, "Overwrite")
        arcpy.gp.Plus_sa(self.i.fac_mf, "1", self.i.fac_po)
        arcpy.BuildRasterAttributeTable_management(self.i.fac_po, "Overwrite")