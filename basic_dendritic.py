import arcpy, ArcHydroTools
from tools import lfp
from time import sleep

class start(object):
    def __init__(self, i, e, n):
        self.i = i
        self.e = e
        self.n = n
        self.run()

    def process_CatchmentPolyProcessing(self):
        print "Please wait..."
        if sleep(90) == None:
            ArcHydroTools.CatchmentPolyProcessing(self.i.cat, self.i.catchment)

    def run(self):
        # self.e.arcpy()
        # self.e.ArcHydroTools()
        self.e.load()
        print "Starting Basic Dendritic processing..."
        ArcHydroTools.FillSinks(self.e.d, self.i.fill, "#", "#", "ISSINK_NO")
        ArcHydroTools.FlowDirection(self.i.fill, self.i.fdr, "")
        ArcHydroTools.FlowAccumulation(self.i.fdr, self.i.fac) 
        arcpy.BuildRasterAttributeTable_management(self.i.fac, "Overwrite")
        ArcHydroTools.StreamDefinition(self.i.fac, self.n, self.i.std)
        ArcHydroTools.StreamSegmentation(self.i.std, self.i.fdr, self.i.sts, "#", "#")
        ArcHydroTools.DrainageLineProcessing(self.i.sts, self.i.fdr, self.i.drl) 
        ArcHydroTools.CatchmentGridDelineation(self.i.fdr, self.i.sts, self.i.cat)
        self.process_CatchmentPolyProcessing()
        lfp.start(self.i, self.e)
        print "Ending Basic Dendritic processing..."