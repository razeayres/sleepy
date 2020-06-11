import arcpy  

class count(object):
    def __init__(self, r):
        self.r = r
        self.data = 0
        self.nodata = 0
        self.run()

    def run(self):
        raster = arcpy.Raster(self.r)
        cnt_pix = raster.height * raster.width
        if raster.isInteger and raster.hasRAT:
            print "[COUNTER]: Integer raster with RAT"
            lst_cnt = [r.COUNT for r in arcpy.SearchCursor(raster)]  
            cnt_data = sum(lst_cnt)
            cnt_nodata = cnt_pix - cnt_data
        else:  
            print "[COUNTER]: Floating raster"  
            arcpy.CheckOutExtension("Spatial")
            ras_isn = arcpy.sa.IsNull(raster)
            arcpy.CheckInExtension("Spatial")
            where = "VALUE = 1"
            lst_cnt = [r.COUNT for r in arcpy.SearchCursor(ras_isn, where_clause=where)]
            cnt_nodata = sum(lst_cnt)
            cnt_data = cnt_pix - cnt_nodata
        self.data = cnt_data
        self.nodata = cnt_nodata
        print "Data pixels  : {0} ({1}%)".format(self.data, round(float(cnt_data) * 100.0 / float(cnt_pix),2))
        print "Nodata pixels: {0} ({1}%)".format(self.nodata, round(float(cnt_nodata) * 100.0 / float(cnt_pix),2))