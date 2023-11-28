from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
import pandas as pd
import numpy as np


from .base_model import AbstractModel



class MeanKNNModel(AbstractModel):
    def __init__(self, n_neighbors: int = 1, **knn_args) -> None:
        super().__init__()
        ct = ColumnTransformer([("one_hot_encoder", OneHotEncoder(sparse_output=False), ["hour"])], remainder='passthrough')
        knn = KNeighborsClassifier(n_neighbors = n_neighbors, **knn_args)
        self.model = make_pipeline(ct, knn)

    def fit(self, typical_data: pd.DataFrame, atypical_data: pd.DataFrame, *args, **kwargs) -> None:
        typical_data = typical_data.groupby(pd.Grouper(key="timestamp", freq="1H")).agg("mean").dropna()
        typical_data["anomaly"] = 0

        atypical_data = atypical_data.groupby(pd.Grouper(key="timestamp", freq="1H")).agg("mean").dropna()
        atypical_data["anomaly"] = 1

        df = pd.concat([typical_data, atypical_data])

        df["hour"] = df.index.hour

        X = df.drop("anomaly", axis=1)
        y = df["anomaly"]

        self.model.fit(X, y)

    def predict(self, data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        data = data.groupby(pd.Grouper(key="timestamp", freq="1H")).agg("mean").dropna()
        data["hour"] = data.index.hour

        ans = pd.DataFrame()
        ans["timestamp"] = data.index
        ans["anomaly_prediction"] = self.model.predict(data)

        return ans
    
    def predict_proba(self, data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        data = data.groupby(pd.Grouper(key="timestamp", freq="1H")).agg("mean").dropna()
        data["hour"] = data.index.hour

        ans = pd.DataFrame()
        ans["timestamp"] = data.index
        ans["anomaly_proba"] = self.model.predict_proba(data)[:, 1]

        return ans
