import arcpy
from tools import classifier

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.Field_Name = "CLASS_NAME"
        self.Field_Type = "TEXT"
        self.l = [(-1, 0),
                  (-1, 22.5, 1),
                  (22.5, 67.5, 2),
                  (67.5, 112.5, 3),
                  (112.5, 157.5, 4),
                  (157.5, 202.5, 5),
                  (202.5, 247.5, 6),
                  (247.5, 292.5, 7),
                  (292.5, 337.5, 8),
                  (337.5, 360, 1)]
        self.run()

    def process_aat_aspect(self):
        classifier.classify(self.i, self.i.aat_aspect, self.l, self.i.aat_aspect_r)
        arcpy.AddField_management(self.i.aat_aspect_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.aat_aspect_r, "CLASS_NAME", self.Field_Name, "VB", "If [VALUE] = 0 Then\\nCLASS_NAME = \"flat\"\\n\\nelseif [VALUE] = 1  Then\\nCLASS_NAME = \"north\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"northeast\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"east\"\\n\\nelseif [VALUE] = 4  Then\\nCLASS_NAME = \"southeast\"\\n\\nelseif [VALUE] = 5  Then\\nCLASS_NAME = \"south\"\\n\\nelseif [VALUE] = 6  Then\\nCLASS_NAME = \"southwest\"\\n\\nelseif [VALUE] = 7  Then\\nCLASS_NAME = \"west\"\\n\\nelseif [VALUE] = 8  Then\\nCLASS_NAME = \"northwest\"\\n\\nelseif [VALUE] = 1  Then\\nCLASS_NAME = \"north\"\\n\\nend if")

    def process_aspect(self):
        classifier.classify(self.i, self.i.aspect, self.l, self.i.aspect_r)
        arcpy.AddField_management(self.i.aspect_r, self.Field_Name, self.Field_Type, "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
        arcpy.CalculateField_management(self.i.aspect_r, "class_name", self.Field_Name, "VB", "If [VALUE] = 0 Then\\nCLASS_NAME = \"flat\"\\n\\nelseif [VALUE] = 1  Then\\nCLASS_NAME = \"north\"\\n\\nelseif [VALUE] = 2  Then\\nCLASS_NAME = \"northeast\"\\n\\nelseif [VALUE] = 3  Then\\nCLASS_NAME = \"east\"\\n\\nelseif [VALUE] = 4  Then\\nCLASS_NAME = \"southeast\"\\n\\nelseif [VALUE] = 5  Then\\nCLASS_NAME = \"south\"\\n\\nelseif [VALUE] = 6  Then\\nCLASS_NAME = \"southwest\"\\n\\nelseif [VALUE] = 7  Then\\nCLASS_NAME = \"west\"\\n\\nelseif [VALUE] = 8  Then\\nCLASS_NAME = \"northwest\"\\n\\nelseif [VALUE] = 1  Then\\nCLASS_NAME = \"north\"\\n\\nend if")

    def run(self):
        self.e.load()
        arcpy.gp.Aspect_sa(self.i.fill_mf, self.i.aspect)
        arcpy.gp.FlowAccumulation_sa(self.i.fdr_mf , self.i.aspect_acc, self.i.aspect, "FLOAT")
        arcpy.gp.Divide_sa(self.i.aspect_acc, self.i.fac_po, self.i.aat_aspect)
        self.process_aat_aspect()
        self.process_aspect()

