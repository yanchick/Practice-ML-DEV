from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
import pandas as pd

from .base_model import AbstractModel



class EmbenddingsModel(AbstractModel):
    def __init__(self) -> None:
         super().__init__()
         self.model = None
     
    def fit(self, typical_data: pd.DataFrame, atypical_data: pd.DataFrame, *args, **kwargs) -> None:
        typical_data = create_emmbenddings(typical_data)
        typical_data["anomaly"] = 0

        atypical_data = create_emmbenddings(atypical_data)
        atypical_data["anomaly"] = 1

        ds = pd.concat([typical_data, atypical_data])

        X = ds.drop("anomaly", axis=1)
        y = ds["anomaly"]

        self.model.fit(X, y)

    def predict(self, data, *args, **kwargs) -> pd.DataFrame:
        data = create_emmbenddings(data)

        ans = pd.DataFrame()
        ans["timestamp"] = data.index
        ans["anomaly_prediction"] = self.model.predict(data)

        return ans
    
    def predict_proba(self, data, *args, **kwargs) -> pd.DataFrame:
        data = create_emmbenddings(data)

        ans = pd.DataFrame()
        ans["timestamp"] = data.index
        ans["anomaly_proba"] = self.model.predict_proba(data)[:, 1]

        return ans


class EmbenddingsKNNModel(EmbenddingsModel):
    def __init__(self, n_neighbors: int = 1, **knn_args) -> None:
        super().__init__()
        ct = ColumnTransformer([("one_hot_encoder", OneHotEncoder(sparse_output=False), ["hour"])], remainder='passthrough')
        knn = KNeighborsClassifier(n_neighbors = n_neighbors, **knn_args)
        self.model = make_pipeline(ct, knn)


class EmbenddingsLinearModel(EmbenddingsModel):
    def __init__(self, max_iter=5000, **log_model_args) -> None:
        super().__init__()
        ct = ColumnTransformer([("one_hot_encoder", OneHotEncoder(sparse_output=False), ["hour"])], remainder='passthrough')
        knn = LogisticRegression(max_iter=max_iter, **log_model_args)
        self.model = make_pipeline(ct, knn)


def create_emmbenddings(data: pd.DataFrame):
        measurements = data.drop("timestamp", axis=1).columns.to_list()

        data = data.groupby(pd.Grouper(key="timestamp", freq="10min")).agg("mean").reset_index()
        data["ten_min"] = data["timestamp"].dt.minute//10
        data["hour"] = data["timestamp"].dt.hour
        data["date"] = data["timestamp"].dt.normalize()
        data = data.pivot(index=["date", "hour"], columns="ten_min", values=measurements)
        data = data.reset_index(1)
        data = data.dropna()
        data.columns = ["_".join([str(j) for j in i if j != ""]) for i in data.columns]

        return data

        









