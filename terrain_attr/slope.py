import arcpy

class start(object):
    def __init__(self, i, e, z):
        self.i = i
        self.e = e
        self.Percent_Rise = "PERCENT_RISE"
        self.Degree = "DEGREE"
        self.zFactor = z
        self.run()

    def process_spr(self):
        arcpy.gp.Slope_sa(self.i.fill_mf, self.i.spr, self.Percent_Rise, self.zFactor)
        arcpy.gp.Int_sa(self.i.spr, self.i.spr_i)
        arcpy.gp.Filter_sa(self.i.spr_i, self.i.spr_f, "LOW", "DATA")
        arcpy.gp.FlowAccumulation_sa(self.i.fdr_mf, self.i.spr_acc,  self.i.spr, "FLOAT")
        arcpy.gp.Divide_sa(self.i.spr_acc, self.i.fac_po, self.i.att_spr)
        arcpy.gp.Int_sa(self.i.att_spr, self.i.att_spr_i)
        arcpy.gp.Filter_sa(self.i.att_spr_i, self.i.att_spr_f, "LOW", "DATA")

    def process_sdg(self):
        arcpy.gp.Slope_sa(self.i.fill_mf, self.i.sdg, self.Degree, self.zFactor)
        arcpy.gp.Int_sa(self.i.sdg, self.i.sdg_i)
        arcpy.gp.Filter_sa(self.i.sdg_i, self.i.sdg_f, "LOW", "DATA")
        arcpy.gp.FlowAccumulation_sa(self.i.fdr_mf, self.i.sdg_acc,  self.i.sdg, "FLOAT")
        arcpy.gp.Divide_sa(self.i.sdg_acc, self.i.fac_po, self.i.att_sdg)
        arcpy.gp.Int_sa(self.i.att_sdg, self.i.att_sdg_i)
        arcpy.gp.Filter_sa(self.i.att_sdg_i, self.i.att_sdg_f, "LOW", "DATA")

    def run(self):
        self.e.load()
        self.process_spr()
        self.process_sdg()


