import joblib
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ColumnConcater(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X['Product Title'].str.lower() + ' ' + X['Cluster Label'].str.lower() + \
            ' Merchant_' + X['Merchant ID'].astype(str)


class BasePredictor:

    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, data: pd.DataFrame):
        data.columns = list(map(str.strip, data.columns))
        return self.model.predict(data)


class CategoryPredictorV001(BasePredictor):
    """
    "Model_001": {
        "model": "LogisticRegression",
        "vectorizer": "CountVectorizer",
        "params": "min_df=20, max_iter=1000",
        "metrics": {
            "cv_accuracy": 0.952,
            "accuracy": 0.97
        },
        "time_prediction_mac_m2": {
            "mean": 0.0004
        }
    }
    """

    def __init__(self, model_path: str = '../models/model__logreg__count_min_df_20_v1.joblib'):
        super().__init__(model_path)


class CategoryPredictorV002(BasePredictor):
    """
    "Model_002": {
        "model": "RandomForestClassifier",
        "vectorizer": "CountVectorizer",
        "params": "min_df=20",
        "metrics": {
            "cv_accuracy": 0.9336,
            "accuracy": 0.961
        },
        "time_prediction_mac_m2": {
            "mean": 0.01374
        }
    }
    """

    def __init__(self, model_path: str = '../models/model__forest__count_min_df_20_v1.joblib'):
        super().__init__(model_path)


class CategoryPredictorV003(BasePredictor):
    """
    "Model_003": {
        "model": "DecisionTreeClassifier",
        "vectorizer": "TfidfVectorizer",
        "params": "default",
        "metrics": {
            "cv_accuracy": 0.923,
            "accuracy": 0.981
        },
        "time_prediction_mac_m2": {
            "mean": 0.0008
        }
    }
    """

    def __init__(self, model_path: str = '../models/model__tree__tfidf_v1.joblib'):
        super().__init__(model_path)


if __name__ == '__main__':
    predictor = CategoryPredictorV003()
    cases = pd.DataFrame({
        ' Category ID': [1, 2, 3],
        ' Category Label': [
            'Apple - MacBook Pro 14" Laptop - M3 Pro chip - 18GB Memory - 14-core GPU - 512G',
            'Roku - 43" Class Select Series 4K Smart RokuTV',
            'Samsung - 15.6 cu. ft. Top Freezer Refrigerator with All-Around Cooling - Stainless Steel'
        ],
        ' Cluster ID': [123, 312, 323],
        ' Cluster Label': ['???', '???', '???'],
        ' Merchant ID': [256, 128, 196],
        'Product ID': [5, 5, 5],
        'Product Title': ['Mobile Phones', 'TVs', 'Fridges'],
    })
    print(predictor.predict(cases))  # ['Mobile Phones', 'TVs', 'Fridges']
    print(type(predictor.predict(cases)))
