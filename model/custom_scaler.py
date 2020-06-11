from pandas import DataFrame
from sklearn.preprocessing import QuantileTransformer

class scaler(object):
    def __init__(self, data):
        qt = QuantileTransformer(output_distribution='normal')
        try:
            self.qt = qt.fit(data)
        except:
            r = [[i] for i in data]
            self.qt = qt.fit(r)
    
    def transform(self, data):
        try:
            r = self.qt.transform(data)
            r = DataFrame(r, index=data.index, columns=data.columns)
            return(r)
        except:
            r = [[i] for i in data]
            r = self.qt.transform(r)
            r = [i[0] for i in r]
            return(r)

    def inverse_transform(self, data):
        try:
            r = self.qt.inverse_transform(data)
            r = DataFrame(r, index=data.index, columns=data.columns)
            return(r)
        except:
            r = [[i] for i in data]
            r = self.qt.inverse_transform(r)
            r = [i[0] for i in r]
            return(r)