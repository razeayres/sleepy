import arcpy, csv
from os import path
from glob import glob
import csv,codecs,cStringIO

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def readrow(self, row):
        r = []
        for s in row:
            try:
                s = str(s)
            except:
                s = s.encode('utf-8', errors="ignore")
            r.append(s)
        return(r)

    def writerow(self, row):
        self.writer.writerow(self.readrow(row))
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.list_rasters()
        self.run()

    def list_rasters(self):
        arcpy.env.workspace = self.e.outputs
        self.rasters = arcpy.ListRasters("*", "GRID")
        # self.rasters = ";".join([" ".join([path.join(self.e.outputs, i), i]) for i in self.rasters if not "_zs" in i])  # txt version
        o = [map(str, [path.join(self.e.outputs, i), i]) for i in self.rasters if not "_zs" in i]
        a = [map(str, [i, path.basename(i).split(".")[0]]) for i in glob(path.join(self.e.auxiliary, "*.tif")) if not "_zs" in i]
        d = [[self.e.d, 'dem']]
        self.rasters = o + a + d    # list version

    def make_zs(self):
        # this part makes
        # zonal statistics from
        # all of the output rasters
        for i in self.rasters:
            self.e.load()
            print("Processing %s..." % i[0].replace(".tif", ""))
            # this creates zonal rasters.
            # Note that it tries to remove
            # the ".tif" extension if it
            # exists in the name of the file
            arcpy.gp.ZonalStatistics_sa(self.i.fc_shp, "OBJECTID", i[0], i[0].replace(".tif", "")+"_zs", "MEAN", "DATA")    # self.i.fc_shp/self.i.facets
            # arcpy.RasterToASCII_conversion(in_raster=i[0]+"_zs",out_ascii_file=i[0]+"_zs"+".txt")   # creates ASCII rasters to be used in modelling

        # this part uses the zonal
        # resampled data to be
        # extracted
        self.rasters = [map(str, [i[0].replace(".tif", "")+"_zs", i[1]]) for i in self.rasters]    # this changes self.rasters

    def prepare(self):
        ### this is to process the observation shapefile ###
        ocs = arcpy.Describe(self.e.d).spatialReference
        while arcpy.Exists(self.i.s):
            arcpy.Delete_management(self.i.s)
        # arcpy.Project_management(self.e.s, self.i.s, ocs)         # this one does not have the gridcode field
        arcpy.Project_management(self.i.fc_shp_osj, self.i.s, ocs)  # this one has the gridcode field
        ####################################################

        #### this is to process the modelling shapefile ####
        while arcpy.Exists(self.i.st):
            arcpy.Delete_management(self.i.st)
        arcpy.FeatureToPoint_management(in_features=self.i.fc_shp, out_feature_class=self.i.st, point_location="INSIDE")    # self.i.fc_shp/self.i.facets
        ####################################################

        self.make_zs()
        arcpy.gp.ExtractMultiValuesToPoints_sa(self.i.s, self.rasters, "NONE")
        arcpy.gp.ExtractMultiValuesToPoints_sa(self.i.st, self.rasters, "NONE")

    def write(self, f, s):
        with open(f, mode='wb') as o:
            fields = [i.name for i in arcpy.ListFields(s)]
            writer = UnicodeWriter(o)
            writer.writerow(fields) # writes the header
            rows = arcpy.da.SearchCursor(s, field_names=fields)  
            for i in rows:
                writer.writerow(i)
            del rows

    def run(self):
        self.e.load()
        print "Exporting table..."
        self.prepare()
        self.write(self.i.tbl_t, self.i.s)
        self.write(self.i.tbl_m, self.i.st)
