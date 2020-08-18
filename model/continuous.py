from pandas import DataFrame, qcut
from numpy import linspace, random, savetxt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV
from sklearn import metrics
import joblib, custom_scaler

from dask.distributed import Client
from dask_ml.model_selection import RandomizedSearchCV

class model(object):
    def __init__(self, name, X, Y, x=None, logger=None, load_save=False):
        self.name = name
        # self.Xt = custom_scaler.scaler(X)
        # self.Yt = custom_scaler.scaler(Y)
        self.X = X
        self.Y = Y
        self.x = x
        self.columns = self.X.columns
        self.logger = logger
        self.load_save = load_save
        self.run()

    def summary(self):
        if not self.hp == None:
            [self.logger.info('Hyperparameter "{kn}" = "{kv}"'.format(kn=i, kv=self.hp[i])) for i in self.hp.keys()]
        self.logger.info("Best predictors = %s" % ", ".join(self.columns[self.model.get_support(indices=True)]))
        self.logger.info("Importances = %s" % ", ".join(map(str, self.model.estimator_.feature_importances_)))
        Y_pred = self.model.predict(self.X_test)
        stats = (metrics.r2_score(self.Y_test, Y_pred),
                 metrics.mean_squared_error(self.Y_test, Y_pred)**0.5,
                 (sum(self.Y_test - Y_pred)/sum(self.Y_test))*100)
        self.logger.info("r2 = %s, RMSE = %s, PBIAS = %s" % stats)

    def train(self):
        seed = random.seed(42)
        bins = qcut(self.Y, 5, labels=False, duplicates='drop')
        X_train, self.X_test, Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.3, stratify=bins, random_state=42)
        estimator = GradientBoostingRegressor(random_state=42)
        selector = RFECV(estimator, cv=2, min_features_to_select=1)
        if self.load_save == True:
            self.logger.warning('The predefined parameters are going to be used')
            self.model = joblib.load(self.name+'.pkl')
            self.hp = None
        else:
            self.logger.warning('The RandomizedSearchCV() is going to be used')
            grid = {'estimator__n_estimators': [int(x) for x in linspace(10, 1000, num = 101)],
                    'estimator__max_depth': [int(x) for x in linspace(1, 100, num = 101)],
                    'estimator__min_samples_split': [int(x) for x in linspace(2, 50, num = 49)],
                    'estimator__min_samples_leaf': [int(x) for x in linspace(2, 50, num = 49)]}
            # client = Client('192.168.200.1:8786')
            self.rscv = RandomizedSearchCV(estimator=selector, param_distributions=grid,
                                           n_iter=50, scoring='r2', cv=2,        # <-- change the number os simulations here! 4000 is the original
                                           iid=False, random_state=42, n_jobs=3)  # , scheduler=client)
            self.rscv.fit(X_train, Y_train)
            self.model = self.rscv.best_estimator_
            joblib.dump(self.model, self.name+'.pkl', compress=1)
            self.hp = self.rscv.best_params_

    def predict(self):
        if isinstance(self.x, DataFrame):
            Y_mod = self.model.predict(self.x)
            self.Y_mod = Y_mod.astype(float)
            # self.Y_mod = self.Yt.inverse_transform(self.Y_mod)
            savetxt(self.name+'.txt', self.Y_mod)
            # df = self.x.copy()
            # df[self.name] = self.Y_mod
            # savetxt(self.name+'.txt', df, header=" ".join(df.columns), comments='')

    def run(self):
        self.logger.info('Starting the %s processing' % self.name)
        self.train()
        self.summary()
        self.predict()