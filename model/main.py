from pandas import DataFrame, to_numeric, concat
from numpy import nan, savetxt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import continuous, discrete
import logging

class main(object):
    def __init__(self, t, m):
        self.t = t
        self.m = m

    def get_metrics(self):
        from sklearn import metrics
        print(metrics.SCORERS.keys())

    def get_lines(self, t):
        reader = open(t, mode='r', encoding='utf-8-sig')
        lines = reader.readlines()
        # pre-processing string lines,
        # removing every noises
        lines = [i.replace('\n', '') for i in lines]
        lines = [i.replace(', ', ':') for i in lines]   # ':' is a temp character
        lines = [i.split(',') for i in lines]
        return(lines)

    def create_df(self, lines):
        # this part removes
        # lines with missing data,
        # and creates the dataframe
        for i, a in enumerate(lines):
            for j, b in enumerate(a):
                if (b == '') or (b == 'None'):
                    lines[i][j] = nan
        df = DataFrame(lines)

        # make the first line
        # the header of the dataframe
        df.columns = df.iloc[0]
        df = df.drop([0])

        # divide the column 'Shape'
        # into 'X' and 'Y'
        shp = df['Shape']
        shp = [(i.replace('"', '')) for i in shp]
        shp = [(i.replace('(', '')) for i in shp]
        shp = [(i.replace(')', '')) for i in shp]
        shp = [(i.split(':')) for i in shp]
        Y = [i[0] for i in shp]
        X = [i[1] for i in shp]

        # replace 'Shape' by 'X' and 'Y'
        # in the dataframe
        df['X'] = X
        df['Y'] = Y
        df = df.drop(columns=['Shape'])
        return(df)

    def make_dataset(self, table, var=None, gridcode=None, additional=[]):
        lines = self.get_lines(table)      # reads the data
        df = self.create_df(lines)      # creates the dataframe
        if not gridcode == None:
            df = df[df['gridcode']==str(gridcode)]       # the subsets are made here.
            # df = df[df[o].duplicated(keep=False)]      # removes the unique values
            df = df.groupby(var).filter(lambda x: len(x)>3)     # removes values with less than 3 replicas
        
        x = ['aat_aspect', 'aspect', 'att_cur', 'att_cur_pf', 'att_cur_pl',
                  'att_sdg_f', 'att_spr_f', 'cti', 'cur', 'cur_pf', 'cur_pl',
                  'sdg', 'spr', 'MOD11A2', 'MOD13A3', 'MOD17A2', 'PCPD', 'PCPSKW',
                  'PCPSTD', 'PCP_MM', 'PR_W1', 'PR_W2', 'dem', 'DEWPT', 'SOLARAV',
                  'WNDAV', 'TMPMX', 'TMPSTDMX', 'TMPMN', 'TMPSTDMN'] + additional

        # impute the data when it is
        # the dataframe for modelling,
        # and thus not for training
        if var == None:
            imp = IterativeImputer(max_iter=100, random_state=42)
            df[x] = df[x].apply(to_numeric, errors='coerce')
            df[x] = imp.fit_transform(df[x])
        df = df.dropna()

        if not var == None:
            y = [i for i in df.columns if i not in x]
            Y = df[var].astype(float)
            X = df[x].astype(float)
            return(X, Y)
        else:
            X = df[x].astype(float)
            return(X)

    def modify_dataset(self, x, series, name=None, Create_LAYER=False):
        # this is to append the data
        # to the modelling dataframe
        x[name] = series

        if Create_LAYER == True:
            for i in set(series):
                duplicates = x[x[name] == i].copy()
                for j in range(1, i):
                    x = x.append(duplicates).sort_index()
            x['LAYER'] = x.groupby(x.index).cumcount() + 1

        return(x)

    def duplicate_dataset(self, X, Y):
        X = X.append(X)
        Y = Y.append(Y)
        return(X, Y)

    def write_results(self):
        x = self.make_dataset(table=self.m)
        x = self.modify_dataset(x, series=self.L_MAX.Y_mod, name='L_MAX', Create_LAYER=True)
        x = self.modify_dataset(x, series=self.SOL_Z.Y_mod, name='SOL_Z')
        x = self.modify_dataset(x, series=self.SOL_SAND.Y_mod, name='SOL_SAND')
        x = self.modify_dataset(x, series=self.SOL_CLAY.Y_mod, name='SOL_CLAY')
        x = self.modify_dataset(x, series=self.SOL_SILT.Y_mod, name='SOL_SILT')
        x = self.modify_dataset(x, series=self.SOL_ROCK.Y_mod, name='SOL_ROCK')
        x = self.modify_dataset(x, series=self.SOL_CBN.Y_mod, name='SOL_CBN')
        x = self.modify_dataset(x, series=self.SB.Y_mod, name='SB')
        x = self.modify_dataset(x, series=self.SOL_SAND.Y_mod, name='SOL_SAND')
        x = self.modify_dataset(x, series=self.CS.Y_mod, name='CS')
        x = self.modify_dataset(x, series=self.FS.Y_mod, name='FS')
        savetxt('output.txt', x, header=" ".join(x.columns), comments='')

    def run(self):
        logging.basicConfig(filename='results.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger('BM')
        # self.get_metrics()

        X, Y = self.make_dataset(table=self.t, var='L_MAX')
        x = self.make_dataset(table=self.m)
        self.L_MAX = discrete.model('L_MAX', X, Y, x, logger=logger, load_save=True)
        del X, Y
        
        X, Y = self.make_dataset(table=self.t, var='SOL_Z', additional=['L_MAX', 'LAYER'])
        X, Y = self.duplicate_dataset(X, Y)
        x = self.modify_dataset(x, series=self.L_MAX.Y_mod, name='L_MAX', Create_LAYER=True)
        self.SOL_Z = continuous.model('SOL_Z', X, Y, x, logger=logger, load_save=True)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='SOL_SAND', additional=['L_MAX', 'LAYER', 'SOL_Z'])
        X, Y = self.duplicate_dataset(X, Y)
        x = self.modify_dataset(x, series=self.SOL_Z.Y_mod, name='SOL_Z')
        self.SOL_SAND = continuous.model('SOL_SAND', X, Y, x, logger=logger, load_save=True)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='SOL_CLAY', additional=['L_MAX', 'LAYER', 'SOL_Z'])
        X, Y = self.duplicate_dataset(X, Y)
        self.SOL_CLAY = continuous.model('SOL_CLAY', X, Y, x, logger=logger, load_save=True)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='SOL_SILT', additional=['L_MAX', 'LAYER', 'SOL_Z'])
        X, Y = self.duplicate_dataset(X, Y)
        self.SOL_SILT = continuous.model('SOL_SILT', X, Y, x, logger=logger, load_save=True)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='SOL_ROCK', additional=['L_MAX', 'LAYER', 'SOL_Z'])
        X, Y = self.duplicate_dataset(X, Y)
        self.SOL_ROCK = continuous.model('SOL_ROCK', X, Y, x, logger=logger, load_save=True)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='SOL_CBN', additional=['L_MAX', 'LAYER', 'SOL_Z'])
        X, Y = self.duplicate_dataset(X, Y)
        self.SOL_CBN = continuous.model('SOL_CBN', X, Y, x, logger=logger, load_save=True)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='SB', additional=['L_MAX', 'LAYER', 'SOL_Z'])
        X, Y = self.duplicate_dataset(X, Y)
        self.SB = continuous.model('SB', X, Y, x, logger=logger)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='CS', additional=['L_MAX', 'LAYER', 'SOL_Z', 'SOL_SAND'])
        X, Y = self.duplicate_dataset(X, Y)
        x = self.modify_dataset(x, series=self.SOL_Z.Y_mod, name='SOL_SAND')
        self.CS = continuous.model('CS', X, Y, x, logger=logger, load_save=True)
        del X, Y

        X, Y = self.make_dataset(table=self.t, var='FS', additional=['L_MAX', 'LAYER', 'SOL_Z', 'SOL_SAND'])
        X, Y = self.duplicate_dataset(X, Y)
        self.FS = continuous.model('FS', X, Y, x, logger=logger, load_save=True)
        del X, Y, x

        self.write_results()

if __name__ == '__main__':
    from dask.diagnostics import ProgressBar
    from dask import config
    from multiprocessing import freeze_support
    freeze_support()
    pbar = ProgressBar()
    pbar.register()
    config.set(scheduler='processes')
    main(r"D:\My_files\SLEEP_Tool\SleepPy\model\training.txt",
        r"D:\My_files\SLEEP_Tool\SleepPy\model\modelling.txt").run()
    pbar.unregister()