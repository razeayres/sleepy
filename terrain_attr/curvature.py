import arcpy
from tools import classifier

class start(object):
    def __init__(self, i, e, z):
        self.i = i
        self.e = e
        self.zFactor = z
        self.Field_Name = "CLASS_NAME"
        self.Field_Type = "TEXT"
        self.l = [(9999, 0, 1),
                  (-9999, 0, 2),
                  (0, 3)]
        self.run()

    def process_cur_pf(self):
        arcpy.gp.FlowAccumulation_sa(self.i.fdr_mf, self.i.cur_pf_acc, self.i.cur_pf, "FLOAT")
        arcpy.gp.Divide_sa(self.i.cur_pf_acc, self.i.fac_po, self.i.att_cur_pf)
        # processing part I
        classifier.classify(self.i, self.i.att_cur_pf, self.l, self.i.att_cur_pf_r)
        arcpy.AddField_management(self.i.att_cur_pf_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.att_cur_pf_r, "CLASS_NAME", self.Field_Name, "VB", "If [VALUE] = 1 Then\\nCLASS_NAME = \"upwardly concave\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"upwardly convex\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"flat\"\\n\\n\\nend if")
        # processing part II
        classifier.classify(self.i, self.i.cur_pf, self.l, self.i.cur_pf_r)
        arcpy.AddField_management(self.i.cur_pf_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.cur_pf_r, "CLASS_NAME", self.Field_Name, "VB", "If [VALUE] = 1 Then\\nCLASS_NAME = \"upwardly concave\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"upwardly convex\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"flat\"\\n\\nend if")

    def process_cur_pl(self):
        arcpy.gp.FlowAccumulation_sa(self.i.fdr_mf, self.i.cur_pl_acc, self.i.cur_pl, "FLOAT")
        arcpy.gp.Divide_sa(self.i.cur_pl_acc, self.i.fac_po, self.i.att_cur_pl)
        # processing part I
        classifier.classify(self.i, self.i.att_cur_pl, self.l, self.i.att_cur_pl_r)
        arcpy.AddField_management(self.i.att_cur_pl_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.att_cur_pl_r, "CLASS_NAME", self.Field_Name, "VB", "If [VALUE] = 1 Then\\nCLASS_NAME = \"upwardly convex\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"upwardly concave\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"flat\"\\n\\n\\nend if")
        # processing part II
        classifier.classify(self.i, self.i.cur_pl, self.l, self.i.cur_pl_r)
        arcpy.AddField_management(self.i.cur_pl_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.cur_pl_r, "CLASS_NAME", self.Field_Name, "VB", "If [VALUE] = 1 Then\\nCLASS_NAME = \"upwardly convex\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"upwardly concave\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"flat\"\\n\\nend if")

    def process_cur(self):
        arcpy.gp.FlowAccumulation_sa(self.i.fdr_mf, self.i.cur_acc, self.i.cur, "FLOAT")
        arcpy.gp.Divide_sa(self.i.cur_acc, self.i.fac_po, self.i.att_cur)
        # processing part I
        classifier.classify(self.i, self.i.att_cur, self.l, self.i.att_cur_r)
        arcpy.AddField_management(self.i.att_cur_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.att_cur_r, "CLASS_NAME", self.Field_Name, "VB", "If [VALUE] = 1 Then\\nCLASS_NAME = \"upwardly convex\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"upwardly concave\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"flat\"\\n\\nend if")
        # processing part II
        classifier.classify(self.i, self.i.cur, self.l, self.i.cur_r)
        arcpy.AddField_management(self.i.cur_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.cur_r, "CLASS_NAME", self.Field_Name, "VB", "If [VALUE] = 1 Then\\nCLASS_NAME = \"upwardly convex\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"upwardly concave\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"flat\"\\n\\nend if")

    def run(self):
        self.e.load()
        arcpy.gp.Curvature_sa(self.i.fill_mf, self.i.cur, self.zFactor, self.i.cur_pf, self.i.cur_pl)
        self.process_cur_pf()
        self.process_cur_pl()
        self.process_cur()

