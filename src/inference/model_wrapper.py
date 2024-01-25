from pathlib import Path
import joblib
import pickle

import pandas as pd
from pandas.core.api import DataFrame as DataFrame


class Model:
    __instance = None

    def predict(self, data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def preprocess(self, data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def load(cls, filename: Path):
        if cls.__instance is None:
            cls.__instance = joblib.load(filename)

        return cls.__instance


class Catboost(Model):
    def __init__(self):
        super().__init__()
        with open(Path(__file__).parent / 'models/catboost.pkl', 'rb') as file:
            self.model = pickle.load(file)

        with open(Path(__file__).parent / 'models/preprocessing_pipeline.pkl', 'rb') as file:
            self.preprocessor = pickle.load(file)

    def predict(self, data: pd.DataFrame, *args, **kwargs):
        return self.model.predict(self.preprocess(data))

    def preprocess(self, df: DataFrame, *args, **kwargs) -> DataFrame:
        df['Age'] = df['Age'] / 365
        df = df.drop('ID', axis=1)
        df['Stage'] = df['Stage'].astype('int64')
        data_scaled = self.preprocessor.transform(df)

        return data_scaled


class RandomForest(Model):
    def __init__(self):
        super().__init__()
        with open(Path(__file__).parent / 'models/random_forest.pkl', 'rb') as file:
            self.model = pickle.load(file)

        with open(Path(__file__).parent / 'models/preprocessing_pipeline.pkl', 'rb') as file:
            self.preprocessor = pickle.load(file)

    def predict(self, data: pd.DataFrame, *args, **kwargs):
        return self.model.predict(self.preprocess(data))

    def preprocess(self, df: DataFrame, *args, **kwargs) -> DataFrame:
        df['Age'] = df['Age'] / 365
        df = df.drop('ID', axis=1)
        df['Stage'] = df['Stage'].astype('int64')
        data_scaled = self.preprocessor.transform(df)

        return data_scaled


class SVC(Model):
    def __init__(self):
        super().__init__()
        with open(Path(__file__).parent / 'models/svc.pkl', 'rb') as file:
            self.model = pickle.load(file)

        with open(Path(__file__).parent / 'models/preprocessing_pipeline.pkl', 'rb') as file:
            self.preprocessor = pickle.load(file)

    def predict(self, data: pd.DataFrame, *args, **kwargs):
        return self.model.predict(self.preprocess(data))

    def preprocess(self, df: DataFrame, *args, **kwargs) -> DataFrame:
        df['Age'] = df['Age'] / 365
        df = df.drop('ID', axis=1)
        df['Stage'] = df['Stage'].astype('int64')
        data_scaled = self.preprocessor.transform(df)

        return data_scaled
