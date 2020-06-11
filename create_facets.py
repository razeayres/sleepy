import arcpy
from time import sleep

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.run()

    def process_c(self, a, b):
        arcpy.gp.MakeFeatureLayer(self.i.catchment, "lyr")
        with arcpy.da.SearchCursor(self.i.cmx, ['HydroID', 'MAX', 'COUNT']) as cursor:
            cursor = sorted(cursor)[:]
            r = []
            for i in cursor:
                if i[1] > i[2]:
                    r.append(i[0])
        q = lambda x: '"HydroID" = %s' % (x)
        qi = map(q, r)
        # --- This code allows for big selections --
        l = len(qi)     # total of elements to be selected
        c = 1000     # number of elements in each chunk
        for i in range(0, l, c):
            if a == self.i.drl:
                if not i+c > l:
                    qs = " OR ".join(qi[i:i+c])
                else:
                    qs = " OR ".join(qi[i:l+1])
            elif a == self.i.lfp:
                if not i+c <= l:
                    qs = " OR ".join(qi[i:i+c])
                else:
                    qs = " OR ".join(qi[i:l+1])
            arcpy.SelectLayerByAttribute_management("lyr", "ADD_TO_SELECTION", qs)
        # --- old code ---
        # qs = " OR ".join(qi)
        # arcpy.SelectLayerByAttribute_management("lyr", "ADD_TO_SELECTION", qs)
        # --- old code ---
        print "Please wait..."
        if sleep(90) == None:   # waits until arcpy.SelectLayerByAttribute_management() is done
            arcpy.Clip_analysis(a, "lyr", b, "")
        arcpy.SelectLayerByAttribute_management("lyr", "CLEAR_SELECTION", "")
        arcpy.Delete_management("lyr")

    def run(self):
        self.e.load()
        print "Starting Creating Facets processing..."
        if arcpy.Exists(self.i.cmx):    # this forces overwriting the cmx table
            arcpy.Delete_management(self.i.cmx)
        arcpy.gp.ZonalStatisticsAsTable_sa(self.i.catchment, "HydroID", self.i.fac, self.i.cmx, "DATA", "MAXIMUM")
        # --- old code ---
        # arcpy.gp.MakeFeatureLayer(self.i.catchment, "lyr")
        # arcpy.AddJoin_management("lyr", "HydroID", self.i.cmx, "HydroID", "KEEP_ALL")
        # arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION","cmx.MAX > cmx.COUNT")
        # arcpy.Clip_analysis(self.i.drl, "lyr", self.i.drl_c, "")
        # arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION","cmx.MAX <= cmx.COUNT")     # ESSA PARTE NAO FOI FEITA
        # arcpy.Clip_analysis(self.i.lfp, "lyr", self.i.lfp_c, "")
        # --- old code ---
        self.process_c(self.i.drl, self.i.drl_c)
        # self.process_c(self.i.lfp, self.i.lfp_c)
        arcpy.Erase_analysis(self.i.drl, self.i.drl_c, self.i.lfp_ct)
        arcpy.SpatialJoin_analysis(target_features=self.i.lfp,join_features=self.i.lfp_ct,out_feature_class=self.i.lfp_c,join_operation="JOIN_ONE_TO_ONE",join_type="KEEP_COMMON",match_option="INTERSECT")
        arcpy.Merge_management(self.i.drl_c + ";" + self.i.lfp_c, self.i.fm_vec)
        arcpy.PolylineToRaster_conversion(self.i.fm_vec, "HydroID", self.i.fm_ras, "MAXIMUM_LENGTH", "NONE", self.e.cs)
        arcpy.gp.Divide_sa(self.i.fm_ras, self.i.fm_ras, self.i.fm_ras_d)
        arcpy.gp.Reclassify_sa(self.i.fm_ras_d, "VALUE", "1 NODATA;NODATA 0", self.i.fm_ras_r, "DATA")
        arcpy.gp.Combine_sa(self.i.fm_ras_r + ";" + self.i.cat, self.i.fm_ras_c)
        arcpy.RasterToPolygon_conversion(self.i.fm_ras_c, self.i.facets, "NO_SIMPLIFY", "VALUE")
        # --- old code ---
        # arcpy.RemoveJoin_management("lyr", "")
        # arcpy.SelectLayerByAttribute_management("lyr", "CLEAR_SELECTION", "")
        # arcpy.Delete_management("lyr")
        # --- old code ---
        print "Ending Creating Facets processing..."