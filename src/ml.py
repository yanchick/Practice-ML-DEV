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


class CategoryPredictor:
    def __init__(self, model_path: str = '../models/model__logreg__count_min_df_20_v1.joblib'):
        self.model = joblib.load(model_path)

    def predict(self, data: pd.DataFrame):
        data.columns = list(map(str.strip, data.columns))
        return self.model.predict(data)


if __name__ == '__main__':
    predictor = CategoryPredictor()
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
    print(type(predictor.predict(cases)))  # 'Mobile Phones
