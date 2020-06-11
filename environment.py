import arcpy, ArcHydroTools
from os import path, makedirs

class setup(object):
    def __init__(self, w, d, s, b):
        self.w = w
        self.d = d
        self.s = s
        self.b = b
        self.cs = arcpy.Describe(self.d).children[0].meanCellHeight
        self.rasters = path.join(self.w, "RASTERS")
        self.vectors = path.join(self.w, "VECTORS.gdb")
        self.outputs = path.join(self.w, "OUTPUTS")
        self.auxiliary = path.join(self.w, "Auxiliary")
        self.temp = path.join(self.w, "TEMP")
        self.temp_r = path.join(self.temp, "RASTERS")
        self.temp_v = path.join(self.temp, "VECTORS.gdb")

    def load(self):
        self.arcpy()
        self.ArcHydroTools()

    def arcpy(self):
        print "Setting arcpy environmental variables...",
        arcpy.env.workspace = self.w
        arcpy.env.scratchWorkspace = self.temp  # changed here from self.w to self.temp
        arcpy.ClearWorkspaceCache_management()
        arcpy.env.snapRaster = self.d
        arcpy.env.extent = arcpy.sa.Raster(self.d).extent
        arcpy.env.cellSize = self.d
        arcpy.env.mask = self.d
        arcpy.env.overwriteOutput = True
        print "OK"

    def ArcHydroTools(self):
        print "Preparing ArcHydroTools extension...",
        ArcHydroTools.SetTargetLocations("HydroConfig", "Layers", self.rasters, self.vectors)
        print "OK"

    def create_folders(self):
        print "Creating containers...",
        if not path.exists(self.rasters):
            makedirs(self.rasters)
        if not path.exists(self.vectors):
            arcpy.CreateFileGDB_management(self.w, "vectors", "CURRENT")
        if not path.exists(self.outputs):
            makedirs(self.outputs)
        if not path.exists(self.temp):
            makedirs(self.temp)
            if not path.exists(self.temp_r):
                makedirs(self.temp_r)
            if not path.exists(self.temp_v):
                arcpy.CreateFileGDB_management(self.temp, "vectors", "CURRENT")
        print "OK"