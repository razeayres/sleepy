import arcpy
import basic, aspect, curvature, slope

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.zFactor = "1"  # "0.00000905"
        self.run()

    def run(self):
        print "Starting Basic Terrain processing..."
        basic.start(self.i, self.e)
        aspect.start(self.i, self.e)
        curvature.start(self.i, self.e, self.zFactor)
        slope.start(self.i, self.e, self.zFactor)
        print "Ending Basic Terrain processing..."