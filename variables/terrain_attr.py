from os import path

class initialize(object):
    def __init__(self, e):
        self.e = e

        self.std_null = path.join(self.e.rasters, "std_null")  # str_isnull
        self.mask = path.join(self.e.rasters, "mask")  # mask
        self.fdr_mf = path.join(self.e.rasters, "fdr_mf")  # fdr_min_fl
        self.fill_mf = path.join(self.e.rasters, "fill_mf")    # fil2_min_fl
        self.fac_mf = path.join(self.e.rasters, "fac_mf")    # fac_min_fl
        self.fac_po = path.join(self.e.rasters, "fac_po")    # Plus_fac_min1
        self.aspect = path.join(self.e.outputs, "aspect")    # aspect0
        self.aspect_acc = path.join(self.e.rasters, "aspect_acc")    # FlowAcc_fdr_1
        self.aat_aspect = path.join(self.e.outputs, "aat_aspect")    # Divide_FlowA1
        self.aat_aspect_r = path.join(self.e.rasters, "aat_aspect_r")    # aataspect
        self.aspect_r = path.join(self.e.rasters, "aspect_r")    # aspect

        self.cur = path.join(self.e.outputs, "cur")    # curv0
        self.cur_pf = path.join(self.e.outputs, "cur_pf")    # profc0
        self.cur_pl = path.join(self.e.outputs, "cur_pl")    # plc0
        self.cur_pf_acc = path.join(self.e.rasters, "cur_pf_acc")    # FlowAcc_fdr_4
        self.att_cur_pf = path.join(self.e.outputs, "att_cur_pf")    # Divide_FlowA4
        self.att_cur_pf_r = path.join(self.e.rasters, "att_cur_pf_r")    # aatprofc
        self.cur_pf_r = path.join(self.e.rasters, "cur_pf_r")    # profc
        self.cur_pl_acc = path.join(self.e.rasters, "cur_pl_acc")    # FlowAcc_fdr_2
        self.att_cur_pl = path.join(self.e.outputs, "att_cur_pl")    # Divide_FlowA2
        self.att_cur_pl_r = path.join(self.e.rasters, "att_cur_pl_r")    # aatplc
        self.cur_pl_r = path.join(self.e.rasters, "cur_pl_r")    # plc
        self.cur_acc = path.join(self.e.rasters, "cur_acc")    # lowAcc_fdr_3
        self.att_cur = path.join(self.e.outputs, "att_cur")    # Divide_FlowA3
        self.att_cur_r = path.join(self.e.rasters, "att_cur_r")    # aatcurv
        self.cur_r = path.join(self.e.rasters, "cur_r")    # curv

        self.spr = path.join(self.e.outputs, "spr")    # slopepct
        self.spr_i = path.join(self.e.rasters, "spr_i")    # pctslp0
        self.spr_f = path.join(self.e.rasters, "spr_f")    # pctslp
        self.spr_acc = path.join(self.e.rasters, "spr_acc")    # FlowAcc_fdr_5
        self.att_spr = path.join(self.e.rasters, "att_spr")    # Divide_FlowA5
        self.att_spr_i = path.join(self.e.rasters, "att_spr_i")    # aatpctslp0
        self.att_spr_f = path.join(self.e.outputs, "att_spr_f")    # aatpctslp

        self.sdg = path.join(self.e.outputs, "sdg")    # slopedeg
        self.sdg_i = path.join(self.e.rasters, "sdg_i")    # degslp0
        self.sdg_f = path.join(self.e.rasters, "sdg_f") # degslp
        self.sdg_acc = path.join(self.e.rasters, "sdg_acc")    # FlowAcc_fdr_6
        self.att_sdg = path.join(self.e.rasters, "att_sdg")    # Divide_FlowA6
        self.att_sdg_i = path.join(self.e.rasters, "att_sdg_i")    # aatdegslp0
        self.att_sdg_f = path.join(self.e.outputs, "att_sdg_f")    # aatdegslp