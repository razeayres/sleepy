from pandas import DataFrame
from numpy import linspace, random, savetxt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV
from sklearn import metrics
from imblearn.over_sampling import SMOTE
import joblib, custom_scaler

from dask.distributed import Client
from dask_ml.model_selection import RandomizedSearchCV

class model(object):
    def __init__(self, name, X, Y, x=None, logger=None, load_save=False):
        self.name = name
        self.X = X
        self.Y = Y
        self.x = x
        self.columns = self.X.columns
        self.logger = logger
        self.load_save = load_save
        self.run()

    def resample(self):
        # This is to resample the data in order
        # to balance it, and improve classifications
        sm = SMOTE(sampling_strategy='not majority', n_jobs=-1, random_state=42)
        self.X, self.Y = sm.fit_resample(self.X, self.Y)

    def summary(self):
        if not self.hp == None:
            [self.logger.info('Hyperparameter "{kn}" = "{kv}"'.format(kn=i, kv=self.hp[i])) for i in self.hp.keys()]
        self.logger.info("Best predictors = %s" % ", ".join(self.columns[self.model.get_support(indices=True)]))
        self.logger.info("Importances = %s" % ", ".join(map(str, self.model.estimator_.feature_importances_)))
        Y_pred = self.model.predict(self.X_test)
        stats = (metrics.accuracy_score(self.Y_test, Y_pred),
                 min(Y_pred),
                 max(Y_pred))
        self.logger.info("Accuracy = %s, min = %s, max = %s" % stats)

    def train(self):
        seed = random.seed(42)
        X_train, self.X_test, Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.3, stratify=self.Y, random_state=42)
        estimator = GradientBoostingClassifier(random_state=42)
        selector = RFECV(estimator, cv=2, min_features_to_select=3)
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
                                           n_iter=400, scoring='accuracy', cv=2,        # <-- change the number os simulations here!
                                           iid=False, random_state=42)  # , scheduler=client)
            self.rscv.fit(X_train, Y_train)
            self.model = self.rscv.best_estimator_
            joblib.dump(self.model, self.name+'.pkl', compress=1)
            self.hp = self.rscv.best_params_

    def predict(self):
        if isinstance(self.x, DataFrame):
            Y_mod = self.model.predict(self.x)
            self.Y_mod = Y_mod.astype(int)
            savetxt(self.name+'.txt', self.Y_mod)
            # df = self.x.copy()
            # df[self.name] = self.Y_mod
            # savetxt(self.name+'.txt', df, header=" ".join(df.columns), comments='')

    def run(self):
        self.logger.info('Starting the %s processing' % self.name)
        self.resample()
        self.train()
        self.summary()
        self.predict()
