import arcpy
from time import sleep

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.Zone_field = "OBJECTID"
        self.Number_of_classes =  6  # self.get_Number_of_classes()   # 6 17
        self.Minimum_class_size = 10
        self.Sample_interval = 10
        self.run()

    # this is highly customizable.
    # In this example, we are using
    # unique profiles to classify
    # the Digital Elevation Model data
    def get_Number_of_classes(self):
        with arcpy.da.SearchCursor(self.e.s, ["FID"]) as cursor:
            rows = [row[0] for row in cursor]
            r = len(rows)
            print "Processing %s classes..." % (r,)
            return(r)

    def process_facet_a_r(self):
        x = arcpy.Raster(self.i.facet_a)
        mn = arcpy.Raster(self.i.facet_mn_a)
        mx = arcpy.Raster(self.i.facet_mx_a)
        out = (x - mn)/(mx - mn)
        out.save(self.i.facet_a_r)

    def process_m_slp_r(self):
        x = arcpy.Raster(self.i.m_slp)
        mn = arcpy.Raster(self.i.m_slp_mn)
        mx = arcpy.Raster(self.i.m_slp_mx)
        out = (x - mn)/(mx - mn)
        out.save(self.i.m_slp_r)

    def process_m_d_r(self):
        x = arcpy.Raster(self.i.m_d)
        mn = arcpy.Raster(self.i.m_d_mn)
        mx = arcpy.Raster(self.i.m_d_mx)
        out = (x - mn)/(mx - mn)
        out.save(self.i.m_d_r)

    def run(self):
        self.e.load()
        print "Starting Facet Classification processing..."
        arcpy.gp.Times_sa(self.i.sdg_f, 0, self.i.empty)
        arcpy.gp.ZonalGeometry_sa(self.i.facets, self.Zone_field, self.i.facet_a, "AREA", self.i.empty)
        arcpy.gp.Int_sa(self.i.empty, self.i.empty_i)
        arcpy.gp.ZonalStatistics_sa(self.i.empty_i, "VALUE", self.i.facet_a, self.i.facet_mn_a, "MINIMUM", "DATA")
        arcpy.gp.ZonalStatistics_sa(self.i.empty_i, "VALUE", self.i.facet_a, self.i.facet_mx_a, "MAXIMUM", "DATA")
        self.process_facet_a_r()

        arcpy.gp.ZonalStatistics_sa(self.i.facets, self.Zone_field, self.i.sdg_f, self.i.m_slp, "MEAN", "DATA")
        arcpy.gp.ZonalStatistics_sa(self.i.empty_i, "VALUE", self.i.m_slp, self.i.m_slp_mn, "MINIMUM", "DATA")
        arcpy.gp.ZonalStatistics_sa(self.i.empty_i, "VALUE", self.i.m_slp, self.i.m_slp_mx, "MAXIMUM", "DATA")
        self.process_m_slp_r()

        arcpy.gp.ZonalStatistics_sa(self.i.facets, self.Zone_field, self.e.d, self.i.m_d, "MEAN", "DATA")
        arcpy.gp.ZonalStatistics_sa(self.i.empty_i, "VALUE", self.i.m_d, self.i.m_d_mn, "MINIMUM", "DATA")
        arcpy.gp.ZonalStatistics_sa(self.i.empty_i, "VALUE", self.i.m_d, self.i.m_d_mx, "MAXIMUM", "DATA")
        self.process_m_d_r()

        print "Please wait...",
        if sleep(180) == None:
            self.e.load()
            print "Processing algorithm...",
            inputs = ";".join([self.i.m_slp_r, self.i.m_d_r])   # only rasters zoned by facets can be entered here
            arcpy.gp.IsoClusterUnsupervisedClassification_sa(self.i.m_slp_r, self.Number_of_classes, self.i.fc, self.Minimum_class_size, self.Sample_interval, self.i.sig)
            arcpy.RasterToPolygon_conversion(self.i.fc, self.i.fc_shp, "NO_SIMPLIFY", "VALUE")
            print "Dissolving...",
            arcpy.Dissolve_management(self.i.fc_shp, self.i.fc_shp_d, "GRIDCODE", "", "MULTI_PART", "DISSOLVE_LINES")
            print "Joining features..."
            # Now it is a point feature
            # instead of a polygon one.
            # This was modified in 11/30/2019
            arcpy.SpatialJoin_analysis(target_features=self.e.s, join_features=self.i.fc_shp_d, out_feature_class=self.i.fc_shp_osj, join_operation="JOIN_ONE_TO_MANY", join_type="KEEP_ALL", match_option="INTERSECT", search_radius="#", distance_field_name="#")
            # arcpy.SpatialJoin_analysis(target_features=self.i.fc_shp_d, join_features=self.e.s, out_feature_class=self.i.fc_shp_osj, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="CLOSEST",search_radius="5000", distance_field_name="#")  # modified match_option="INTERSECT" in 06/15/2019 to "CLOSEST"
        print "Ending Facet Classification processing..."