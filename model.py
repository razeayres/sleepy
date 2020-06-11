from pandas import DataFrame, qcut
from numpy import nan, linspace, random
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_selection import SelectKBest, f_regression, f_classif
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics


class model(object):
    def __init__(self, df):
        self.df = df
        self.x = ['aat_aspect', 'aspect', 'att_cur', 'att_cur_pf', 'att_cur_pl', 'att_sdg_f', 'att_spr_f', 'cti', 'cur', 'cur_pf', 'cur_pl', 'sdg', 'spr', 'MOD11A2', 'MOD13A3', 'MOD17A2', 'PCPD', 'PCPSKW', 'PCPSTD', 'PCP_MM', 'PR_W1', 'PR_W2', 'dem', 'DEWPT', 'SOLARAV', 'WNDAV', 'TMPMX', 'TMPSTDMX', 'TMPMN', 'TMPSTDMN']
        self.y = [i for i in self.df.columns if i not in self.x]
        self.make_dataset('L_MAX') # L_MAX SOL_ZMAX
        self.regressor()
        self.make_dataset('L_MAX') # L_MAX SOL_ZMAX
        self.classifier()

    def make_dataset(self, i):
        self.Y = self.df[i].astype(float)
        self.X = self.df[self.x].astype(float)

    def regressor(self):
        seed = random.seed(42)
        bins = qcut(self.Y, 4, labels=False, duplicates='drop')
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y, test_size=0.3, stratify=bins)     # , stratify=bins)
        print('Sizes of train and test: %s, %s.' % (len(X_train), len(X_test)))

        kbest = SelectKBest(f_regression)
        rf = RandomForestRegressor(n_jobs=-1, n_estimators=1000)
        pipe = make_pipeline(kbest, rf)

        grid = {'selectkbest__k': [int(x) for x in linspace(3, 30, num = 28)],
                'randomforestregressor__max_depth': [int(x) for x in linspace(1, 250, num = 251)] + [None],
                'randomforestregressor__min_samples_split': [int(x) for x in linspace(2, 30, num = 29)],
                'randomforestregressor__min_samples_leaf': [int(x) for x in linspace(2, 30, num = 29)]}
        self.model = RandomizedSearchCV(estimator=pipe, param_distributions=grid, n_iter=3000, scoring='r2', cv=3, n_jobs=-1, iid=False)
        self.model.fit(X_train, Y_train)
        print("best pars =", self.model.best_params_)
        Y_pred = self.model.predict(X_test)
        print("r2 =", round(metrics.r2_score(Y_test, Y_pred), 2), "RMSE =", round(metrics.mean_squared_error(Y_test, Y_pred)**0.5, 2))

    def classifier(self):
        seed = random.seed(42)
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y, test_size=0.3)
        print('Sizes of train and test: %s, %s.' % (len(X_train), len(X_test)), "min =", min(Y_train),"max =", max(Y_train))

        scaler = MinMaxScaler(feature_range = (0,1))
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        self.model = RandomForestClassifier(n_jobs=-1, n_estimators=1000, class_weight='balanced')

        self.model.fit(X_train, Y_train)
        Y_pred = self.model.predict(X_test)
        print("Accuracy =", round(metrics.accuracy_score(Y_test, Y_pred), 2), "min =", min(Y_pred),"max =", max(Y_pred))


class main(object):
    def __init__(self):
        self.t = r"D:\My_files\Meus_artigos\Em_andamento\Artigo_de_solos_2019\Projetos\Pernambuco\OUTPUTS\table.txt"
        self.run()

    def read(self):
        reader = open(self.t, 'r')
        lines = reader.readlines()
        # pre-processing string lines,
        # removing every noises
        lines = [i.replace('\n', '') for i in lines]
        lines = [i.replace(', ', ':') for i in lines]   # ':' is a temp character
        lines = [i.split(',') for i in lines]

        # this part removes
        # lines with missing data,
        # and creates the dataframe
        for i, a in enumerate(lines):
            for j, b in enumerate(a):
                if '' == b:
                    lines[i][j] = nan
        df = DataFrame(lines).dropna()

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

        self.df = df[df['gridcode']=='1']

    def run(self):
        self.read()
        # print(metrics.SCORERS.keys())
        m = model(self.df)

main()
