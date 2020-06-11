from os import path

class initialize(object):
    def __init__(self, e):
        self.e = e

        self.empty = path.join(self.e.rasters, "empty")  # empty
        self.facet_a = path.join(self.e.rasters, "facet_a")  # facetarea
        self.empty_i = path.join(self.e.rasters, "empty_i")  # emptyint
        self.facet_mn_a = path.join(self.e.rasters, "facet_mn_a")  # minfacarea
        self.facet_mx_a = path.join(self.e.rasters, "facet_mx_a")  # maxfacarea
        self.facet_a_r = path.join(self.e.rasters, "facet_a_r")  # RescFacArea
        self.m_slp = path.join(self.e.rasters, "m_slp")  # MeanSlope
        self.m_slp_mn = path.join(self.e.rasters, "m_slp_mn")  # minmeanslope
        self.m_slp_mx = path.join(self.e.rasters, "m_slp_mx")  # maxmeanslope
        self.m_slp_r = path.join(self.e.rasters, "m_slp_r")  # RescMeanSlp
        self.m_d = path.join(self.e.rasters, "m_d")
        self.m_d_mn = path.join(self.e.rasters, "m_d_mn")
        self.m_d_mx = path.join(self.e.rasters, "m_d_mx")
        self.m_d_r = path.join(self.e.rasters, "m_d_r")
        self.fc = path.join(self.e.outputs, "fc")    # FacetClass
        self.sig = path.join(self.e.outputs, "sig")    # signature_gsg
        self.fc_shp = path.join(self.e.vectors, "fc_shp")    # Facet_Classification_Shapefile
        self.fc_shp_d = path.join(self.e.vectors, "fc_shp_d")    # Facet_Classification_Diss_shp
        self.fc_shp_osj = path.join(self.e.vectors, "fc_shp_osj")  # Facet_Soil_Obs_Spatial_Join