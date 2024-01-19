from pathlib import Path
import pickle
import joblib

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from sklearn.preprocessing import StandardScaler


class Model():
    __instance = None
    
    def predict(self, data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def preprocess(self, data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def load(cls, filename: Path):
        if cls.__instance is None:
            cls.__instance = joblib.load(filename)

        return cls.__instance

class Lasso(Model):
    def __init__(self):
        super().__init__()
        self.model = self.load(Path(__file__).parent / 'models/lasso_model.pkl')
        self.scaler = StandardScaler()

    def predict(self, data: pd.DataFrame, *args, **kwargs):
        return self.model.predict(self.preprocess(data))[0]

    def preprocess(self, data: DataFrame, *args, **kwargs) -> DataFrame:
        data['Sex'] = data['Sex'].replace({'M':0, 'F':1})
        data['Ascites'] = data['Ascites'].replace({'N':0, 'Y':1})
        data['Drug'] = data['Drug'].replace({'D-penicillamine':0, 'Placebo':1})
        data['Hepatomegaly'] = data['Hepatomegaly'].replace({'N':0, 'Y':1})
        data['Spiders'] = data['Spiders'].replace({'N':0, 'Y':1})
        data['Edema'] = data['Edema'].replace({'N':0, 'Y':1, 'S':-1})
        data['Status'] = data['Status'].replace({'C':0, 'CL':1, 'D':-1})
        data['Age'] = data['Age'] / 365
        data = data.drop(['Status', 'ID'], axis=1)
        data_scaled = self.scaler.fit_transform(data)

        return data_scaled
