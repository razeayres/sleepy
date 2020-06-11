import arcpy, ArcHydroTools
from time import sleep

class start(object):
    def __init__(self, i, e):
        self.i = i
        self.e = e
        self.run()

    def process_l_lmx(self):
        # arcpy.gp.ZonalStatistics_sa(self.i.l_ild, "Value", self.i.l_fln, self.i.l_lmx, "MAXIMUM", "DATA")
        arcpy.BuildRasterAttributeTable_management(self.i.l_ild, "Overwrite")
        stats = arcpy.sa.ZonalStatistics(self.i.l_ild, "Value", self.i.l_fln, "MAXIMUM", "DATA")
        stats.save(self.i.l_lmx)

    def create_lfp(self):
        arcpy.gp.FocalStatistics_sa(self.i.cat, self.i.l_rng, "Rectangle 1 1 CELL", "RANGE", "DATA")    # distance from boundaries
        arcpy.gp.Con_sa(self.i.l_rng, self.i.cat, self.i.l_ild, "#", "Value = 0")
        arcpy.gp.IsNull_sa(self.i.l_ild, self.i.l_ild_n)
        arcpy.gp.ExtractByMask_sa(self.i.l_ild_n, self.i.cat, self.i.l_ild_n_c)
        arcpy.gp.Con_sa(self.i.l_ild_n_c, self.e.d, self.i.l_fnd, "#", "Value = 0")
        arcpy.gp.Fill_sa(self.i.l_fnd, self.i.l_fill, "")
        arcpy.gp.FlowDirection_sa(self.i.l_fill, self.i.l_fdr, "NORMAL", "")
        arcpy.gp.FlowLength_sa(self.i.l_fdr, self.i.l_fln, "DOWNSTREAM", "")
        self.process_l_lmx()
        arcpy.gp.EqualTo_sa(self.i.l_lmx, self.i.l_fln, self.i.l_lmx_fln)
        arcpy.gp.Con_sa(self.i.l_lmx_fln, self.i.l_ild, self.i.l_mxp_r, "#", "Value = 1")
        arcpy.RasterToPoint_conversion(in_raster=self.i.l_mxp_r, out_point_features=self.i.l_mxp_v, raster_field="Value")
        arcpy.CopyFeatures_management(in_features=self.i.l_mxp_v, out_feature_class=self.i.generate_temps("v", "mxp"))
        arcpy.DeleteIdentical_management(in_dataset=self.i.l_mxp_v, fields="GRID_CODE", xy_tolerance="", z_tolerance="0")
        arcpy.gp.CostPath_sa(self.i.l_mxp_v, self.i.fdr, self.i.fdr, self.i.l_pth, "EACH_CELL", "GRID_CODE")    # main function
        print "Please wait...",
        if sleep(90) == None:
            arcpy.gp.StreamToFeature_sa(self.i.l_pth, self.i.fdr, self.i.l_lfp, "NO_SIMPLIFY")
            arcpy.SpatialJoin_analysis(target_features=self.i.l_lfp,join_features=self.i.catchment,out_feature_class=self.i.l_spa,join_operation="JOIN_ONE_TO_ONE",join_type="KEEP_ALL",match_option="HAVE_THEIR_CENTER_IN")

    def prepare_lfp(self):
        arcpy.gp.MakeFeatureLayer(self.i.l_spa, "lyr")
        with arcpy.da.SearchCursor("lyr", ['OBJECTID', 'GridID', 'Shape_Length', 'to_node', 'HydroID']) as cursor:
            cursor = sorted(cursor)[:]
            GridID = [i[1] for i in cursor]
            for i in set(GridID):
                if GridID.count(i) > 1:
                    to_node = [j[3] for j in cursor if (j[1] == i)]
                    for j in set(to_node):
                        if to_node.count(j) > 1:
                            Shape_Length = [l[2] for l in cursor if (l[1] == i) and (l[3] == j)]
                            s = [l[0] for l in cursor if l[2] == min(Shape_Length)][0]
                            arcpy.SelectLayerByAttribute_management("lyr", "ADD_TO_SELECTION", "OBJECTID = " + str(s))
            self.HydroID = max([i[4] for i in cursor]) + 1
            arcpy.DeleteFeatures_management("lyr")
            arcpy.SelectLayerByAttribute_management("lyr", "CLEAR_SELECTION", "")
        for i in arcpy.ListFields("lyr"):
            if i.name not in ['OBJECTID', 'Shape', 'Shape_Length', 'HydroID']:
                arcpy.DeleteField_management("lyr", i.name)
        arcpy.Dissolve_management(in_features="lyr",out_feature_class=self.i.lfp,dissolve_field="HydroID",statistics_fields="#",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")
        arcpy.Delete_management("lyr")

    def finalize_lfp(self):
        arcpy.gp.MakeFeatureLayer(self.i.lfp, "lyr")
        arcpy.AddField_management("lyr", "DrainID", "LONG")
        cursor = arcpy.UpdateCursor(dataset="lyr", sort_fields="HydroID A")
        for i in cursor:
            v = i.getValue('HydroID')
            i.setValue('DrainID', v)
            i.setValue('HydroID', self.HydroID)
            cursor.updateRow(i)
            self.HydroID += 1
        arcpy.Delete_management("lyr")

    def run(self):
        self.e.load()
        print "Processing the longest flow...",
        self.create_lfp()
        self.prepare_lfp()
        self.finalize_lfp()
        print "OK"