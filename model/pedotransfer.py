from glob import glob
from os import path
import pandas, numpy

class dataset(object):
    def __init__(self, workdir):
        self.workdir = workdir
        self.output = path.join(self.workdir,"output.txt")
        self.df = pandas.read_csv(self.output, delimiter=' ')

class model(object):
    def __init__(self, df):
        self.df = df.df
        self.prepare_dataset()
        self.run()

    def get_stats(self, i, var='hist.txt', hist=False):
        if hist == True:
            n = 10000
            y = numpy.histogram(i, bins=n)
            x = numpy.linspace(min(i), max(i), num=n)
            data = [i for i in zip(x, y[0])]
            numpy.savetxt('h_' + var, data)
        return(var, i.mean(), numpy.std(i), max(i), min(i))

    def count_invalid(self, t, var):
        c = numpy.count_nonzero(numpy.where(var < t, 0, 1))
        n = c/len(var)
        n = (1-n)*100
        n = round(n, 4)
        return('%s%% is of invalid values' % n)

    def summary_dataset(self):
        for i in [(self.L_MAX, 'L_MAX'),
                  (self.SOL_Z, 'SOL_Z'),
                  (self.SOL_SAND, 'SOL_SAND'),
                  (self.SOL_CLAY, 'SOL_CLAY'),
                  (self.SOL_SILT, 'SOL_SILT'),
                  (self.SOL_ROCK, 'SOL_ROCK'),
                  (self.SOL_CBN, 'SOL_CBN'),
                  (self.SB, 'SB'),
                  (self.CS, 'CS'),
                  (self.FS, 'FS')]:
            a, n = i
            print(self.get_stats(a, n), self.count_invalid(0, a))

    def prepare_dataset(self):
        self.L_MAX = self.df['L_MAX']
        self.SOL_Z = self.df['SOL_Z']
        self.SOL_SAND = self.df['SOL_SAND']
        self.SOL_CLAY = self.df['SOL_CLAY']
        self.SOL_SILT = self.df['SOL_SILT']
        self.SOL_ROCK = self.df['SOL_ROCK']
        self.SOL_CBN = self.df['SOL_CBN']
        self.SB = self.df['SB']
        self.CS = self.df['CS']
        self.FS = self.df['FS']

        # this is to correct variables
        # adding values proportionally
        # of the depth
        for var in ['SOL_Z', 'SOL_CBN', 'SB', 'SOL_SAND', 'SOL_CLAY', 'SOL_SILT', 'SOL_ROCK', 'CS', 'FS']:
            self.df['GRIDCODE'] = self.df['LAYER'].eq(1).cumsum()
            min_values = self.df.groupby('GRIDCODE').min()[var]
            min_value = min(self.df['GRIDCODE'])
            min_pkg = zip(set(self.df['GRIDCODE']), min_values)
            for i in min_pkg:
                if i[1]<=0:
                    self.df.loc[self.df.GRIDCODE == i[0], var]+=abs(i[1])+min_value
            cmd = 'self.' + var + ' = numpy.round(numpy.array(self.df["' + var + '"]), 6)'
            exec(cmd)

        # self.SOL_SAND = numpy.where(self.SOL_SAND > 100, 100, self.SOL_SAND)     # method 2
        grl_pkg = list(zip(self.SOL_SAND, self.SOL_CLAY, self.SOL_SILT, self.CS, self.FS))
        for i in range(len(grl_pkg)):
            s = self.SOL_SAND[i]+self.SOL_CLAY[i]+self.SOL_SILT[i]
            # s_cs = self.SOL_CLAY[i]+self.SOL_SILT[i]     # method 2
            if s > 100:
                self.SOL_SAND[i] = (self.SOL_SAND[i]/s)*100     # method 1
                self.SOL_CLAY[i] = (self.SOL_CLAY[i]/s)*100     # method 1
                self.SOL_SILT[i] = (self.SOL_SILT[i]/s)*100     # method 1
                # self.SOL_CLAY[i] = (self.SOL_CLAY[i]/s_cs)*(100-self.SOL_SAND[i])     # method 2
                # self.SOL_SILT[i] = (self.SOL_SILT[i]/s_cs)*(100-self.SOL_SAND[i])     # method 2
                self.SOL_ROCK[i] = 0
            else:
                self.SOL_ROCK[i] = 100 - s

            s = self.CS[i]+self.FS[i]
            self.CS[i] = (self.CS[i]/s)*100
            self.FS[i] = (self.FS[i]/s)*100

        self.OM = self.SOL_CBN * 2
        # self.summary_dataset()

    def calc_SOL_ALB(self):
        ### this equation is checked ###
        # Baumer (1990) 
        self.SOL_ALB = 0.6/numpy.exp(0.4*self.OM)
        print(self.get_stats(self.SOL_ALB, var='ALB', hist=True))

    def calc_USLE_K(self):
        ### this equation is checked ###
        # Sharpley and Williams (1990)
        SN1 = 1-(self.SOL_SAND/100)
        self.USLE_K = ((0.2 + 0.3 * numpy.exp(-0.0256 * self.SOL_SAND * (1 - (self.SOL_SILT/100)))) * 
                      (self.SOL_SILT/(self.SOL_CLAY + self.SOL_SILT))**0.3 *
                      (1 - ((0.25 * self.SOL_CBN)/(self.SOL_CBN + numpy.exp(3.72 - 2.95 * self.SOL_CBN)))) *
                      (1 - ((0.7  *SN1)/(SN1 + numpy.exp(-5.51 + 22.9 * SN1)))))
        print(self.get_stats(self.USLE_K, var='USLE_K', hist=True))

    def calc_SOL_K(self, method='', t_33=None, t_1500=None, t_s=None):
        ### this equation is checked ###
        ########################
        # this requires t_33   #
        # t_1500 and t_3       #
        ########################
        # Saxton and Rawls (2006)
        if method == 'SR2006':
            B = (numpy.log(1500) - numpy.log(33))/(numpy.log(t_33) - numpy.log(t_1500))
            g = 1/B
            self.SOL_K = 1930 * (t_s - t_33)**(3-g)

        ### this equation is checked ###
        # Belk et al. (2007)
        elif method == 'BK2007':
            self.SOL_K = (58 * (self.SOL_Z/1000)**-0.9) # SOL_Z must be converted from mm to m
            self.SOL_K = (self.SOL_K*10)/24 # that converts from cm/day to mm/hr

    def calc_SOL_BD(self, method=''):
        ### this equation is checked ###
        # Saxton and Rawls (2006) = SR2006
        if method == 'SR2006':
            t_s33t = (0.278 * (self.SOL_SAND/100) +
                      0.034 * (self.SOL_CLAY/100) +
                      0.022 * self.OM -
                      0.018 * ((self.SOL_SAND/100) * self.OM) -
                      0.027 * ((self.SOL_CLAY/100) * self.OM) -
                      0.584 * ((self.SOL_SAND/100) * (self.SOL_CLAY/100)) +
                      0.078)
            t_s33 = t_s33t + (0.636 * t_s33t - 0.107)

            t_33t = (-0.251 * (self.SOL_SAND/100) +
                      0.195 * (self.SOL_CLAY/100) +
                      0.011 * self.OM +
                      0.006 * ((self.SOL_SAND/100) * self.OM) -
                      0.027 * ((self.SOL_CLAY/100) * self.OM) +
                      0.452 * ((self.SOL_SAND/100) * (self.SOL_CLAY/100)) +
                      0.299)
            t_33 = t_33t + (1.283 * t_33t**2 - 0.374 * t_33t - 0.015)

            t_s = t_33 + t_s33 - 0.097 * (self.SOL_SAND/100) + 0.043
            pn = (1 - t_s) * 2.65

            rw = self.SOL_ROCK/100
            pr = pn/2.65
            rv = (pr * rw)/(1 - rw * (1 - pr))

            self.SOL_BD = pn * (1 - rv) + (rv * 2.65)
            print(self.get_stats(self.SOL_BD, var='BD_SR2006', hist=True))

            self.t_33 = t_33    # global var
            self.t_s = t_s    # global var
            self.rv = rv    # global var

        ### this equation is checked ###
        # Oliveira et al. (2002) = OL2002
        elif method == 'OL2002':
            self.SOL_BD = numpy.where(self.SOL_Z > 300, 
                                      1.5574 - 0.0005 * (self.SOL_CLAY*10) - 0.006 * (self.SOL_CBN*10) + 0.0076 * self.SB,
                                      1.5544 - 0.0004 * (self.SOL_CLAY*10) - 0.01 * (self.SOL_CBN*10) + 0.0067 * self.SB)
            print(self.get_stats(self.SOL_BD, var='BD_OL2002', hist=True))

    def calc_SOL_AWC(self, method=''):
        ### this equation is checked ###
        # Saxton and Rawls (2006) = SR2006
        if method == 'SR2006':
            t_1500t = (-0.024 * (self.SOL_SAND/100) +
                        0.487 * (self.SOL_CLAY/100) +
                        0.006 * self.OM +
                        0.005 * ((self.SOL_SAND/100) * self.OM) -
                        0.013 * ((self.SOL_CLAY/100) * self.OM) +
                        0.068 * ((self.SOL_SAND/100) * (self.SOL_CLAY/100)) +
                        0.031)
            t_1500 = t_1500t + (0.14 * t_1500t - 0.02)
            print(self.count_invalid(0, t_1500))
            t_1500 = numpy.where(t_1500 <= 0, 0.00001, t_1500)    # <-- this is based on the Fig. 1 of Saxton and Rawls (2006)

            self.SOL_AWC = (self.t_33 - t_1500) * (1 - self.rv)
            print(self.get_stats(self.SOL_AWC, var='AWC_SR2006', hist=True))

            self.calc_SOL_K(method='SR2006', t_33=self.t_33, t_1500=t_1500, t_s=self.t_s)
            print(self.get_stats(self.SOL_K, var='K_SR2006', hist=True))

        ### this equation is checked ###
        # Oliveira et al. (2006) = OL2006
        elif method == 'OL2006':
            # we multiply here by 10 to convert
            # from kg/kg (e.g. SOL_SAND/100) to
            # g/kg (1 k/kg = 1000 g/kg)
            ### (x/100)*1000 == x*10 ###
            self.SOL_AWC = (-0.000021 * (self.SOL_SAND*10) +
                             0.000203 * (self.SOL_SILT*10) +
                             0.000054 * (self.SOL_CLAY*10) +
                             0.021656 * self.SOL_BD)

            print(self.get_stats(self.SOL_AWC, var='AWC_OL2006', hist=True))

        # Barros et al. (2013) = BR2013
        elif method == 'BR2013':
            t_r = (0.0858 -
                   0.1671 * (self.SOL_SAND/100) +
                   0.3516 * (self.SOL_CLAY/100) +
                   1.1846 * (self.OM/100) +
                   0.000029 * (self.SOL_BD/1000))
            print(self.count_invalid(0, t_r))
            t_r = numpy.where(t_r <= 0, 0.01, t_r)    # <-- this is based on the Table 3 of Barros et al. (2013)
            t_s = 1 - 0.00037 * (self.SOL_BD/1000)
            a = 10**(0.8118 +
                     0.8861 * (self.SOL_SAND/100) -
                     1.1907 * (self.SOL_CLAY/100) -
                     0.001514 * (self.SOL_BD/1000))
            n = (1.1527 + 
                 0.7427 * (self.SOL_SAND/100) +
                 0.4135 * (self.SOL_SILT/100) -
                 5.5341 * (self.OM/100))
            m = 1 - (1/n)

            t_33 = (t_r + ((t_s - t_r)/
                   ((1 + (a * 33)**n)**m)))
            t_1500 = (t_r + ((t_s - t_r)/
                   ((1 + (a * 1500)**n)**m)))
            self.SOL_AWC = t_33 - t_1500

            print(self.get_stats(self.SOL_AWC, var='AWC_BR2013', hist=True))
            self.calc_SOL_K(method='SR2006', t_33=t_33, t_1500=t_1500, t_s=t_s)
            print(self.get_stats(self.SOL_K, var='K_SR2006_BR2013', hist=True))

        ### this equation is checked ###
        # Tomasella et al. (2000) = TM2000
        elif method == 'TM2000':
            t_r = (23.3867 +
                   0.1103 * self.SOL_CLAY -
                   4.7949 * self.SOL_BD +
                   0.0047 * (self.SOL_SILT * self.SOL_CLAY) -
                   0.0027 * self.CS**2 - 
                   0.0022 * self.FS**2 -
                   0.0048 * self.SOL_SILT**2)/100
            print(self.count_invalid(0, t_r))
            t_r = numpy.where(t_r <= 0, 0.0001, t_r)    # <-- this is based on the Table 3 of Tomasella et al. (2000)
            t_s = (91.6203-
                   30.0046 * self.SOL_BD +
                   1.5925 * self.SOL_CBN +
                   0.0022 * (self.CS*self.SOL_SILT) -
                   0.0036 * (self.CS*self.SOL_CLAY) -
                   0.0018 * self.CS**2 -
                   0.001 * self.FS**2)/100
            a = numpy.exp((205.6546 -
                           2.556 * self.SOL_SILT -
                           0.1329 * self.SOL_CLAY -
                           247.4904 * self.SOL_BD -
                           0.0189 * (self.CS*self.FS) +
                           0.1177 * (self.CS*self.SOL_SILT) +
                           0.0517 * (self.FS*self.SOL_CLAY) +
                           0.0617 * self.CS**2)/100)
            n = (168.8617 -
                 0.0258 * (self.CS*self.SOL_SILT) -
                 0.0261 * (self.FS*self.SOL_CLAY) +
                 0.0093 * self.FS**2 -
                 0.0077 * self.SOL_SILT**2)/100
            print(self.count_invalid(1, n))
            n = numpy.where(n <= 1, 1.0001, n)    # <-- this is based on the Table 3 of Tomasella et al. (2000)
            m = 1 - (1/n)

            t_33 = (t_r + ((t_s - t_r)/
                   ((1 + (a * 33)**n)**m)))
            t_1500 = (t_r + ((t_s - t_r)/
                   ((1 + (a * 1500)**n)**m)))
            self.SOL_AWC = t_33 - t_1500

            print(self.get_stats(self.SOL_AWC, var='AWC_TM2000', hist=True))
            self.calc_SOL_K(method='SR2006', t_33=t_33, t_1500=t_1500, t_s=t_s)
            print(self.get_stats(self.SOL_K, var='K_SR2006_TM2000', hist=True))

    def run(self):
        self.calc_SOL_ALB()
        self.calc_USLE_K()

        self.calc_SOL_BD(method='SR2006')
        self.calc_SOL_AWC(method='SR2006')  

        self.calc_SOL_BD(method='OL2002')
        self.calc_SOL_AWC(method='OL2006')
        self.calc_SOL_AWC(method='BR2013')
        self.calc_SOL_AWC(method='TM2000')

        self.calc_SOL_K(method='BK2007')
        print(self.get_stats(self.SOL_K, var='K_BK2007', hist=True))

df = dataset("D:\My_files\SLEEP_Tool\SleepPy\model")
model(df)