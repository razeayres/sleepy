import arcpy
import basic_dendritic, create_facets, terrain_attr, class_facets, cti, postprocessing
from os import chdir

class start(object):
    def __init__(self, i, e, n):
        self.i = i
        self.e = e
        self.n = n
        self.run()

    def run(self):
        self.e.create_folders()
        chdir(self.e.temp)   # changes workdir to temp
        self.e.load()
        self.Spatial_CheckOut()     # do not comment this!
        # basic_dendritic.start(self.i, self.e, self.n)
        # create_facets.start(self.i, self.e)
        # terrain_attr.start(self.i, self.e)
        # class_facets.start(self.i, self.e)
        # cti.start(self.i, self.e)
        postprocessing.start(self.i, self.e)
        self.Spatial_CheckIn()     # do not comment this!

    def Spatial_CheckOut(self):
        print "Checking out Spatial extension...",
        arcpy.CheckOutExtension("Spatial")
        print "OK"

    def Spatial_CheckIn(self):
        print "Checking in Spatial extension...",
        arcpy.CheckInExtension("Spatial")
        print "OK"