import arcpy

class classify(object):
    def __init__(self, i, e, l, o):
        self.i = i
        self.l = l
        self.e = e
        self.o = o
        self.con()

    def temp(self, i):
        if i == self.l[0]:
            self.s = self.i.temp0
        else:
            self.e = self.s
            if self.e == self.i.temp1:
                self.s = self.i.temp0
            elif self.e == self.i.temp0:
                self.s = self.i.temp1
        return(False)

    def clear(self):
        try:
            arcpy.Delete_management(self.i.temp0)
            arcpy.Delete_management(self.i.temp1)
        except:
            pass

    def save(self):
        # arcpy.Copy_management(self.s, self.o)
        r = arcpy.sa.Int(self.s)
        r.save(self.o)

    def con(self):
        self.clear()
        for i in self.l:
            self.temp(i)
            if len(i) == 3:
                arcpy.gp.Con_sa(self.e, str(i[2]), self.s, self.e, '"' + "Value" + '" > ' + str(i[0]) + " AND " + '"' + "Value" + '" <= ' + str(i[1] + 0.01))
            else:
                arcpy.gp.Con_sa(self.e, str(i[1]), self.s, self.e, '"' + "Value" + '"=' + str(i[0]))
        self.save()
        self.clear()