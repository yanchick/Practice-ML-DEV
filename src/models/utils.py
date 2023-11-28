from sklearn.model_selection import train_test_split
import pandas as pd


def train_test_split_by_hours(data: pd.DataFrame, **train_test_split_kwargs):

    train_hours, test_hours = train_test_split(data.groupby(pd.Grouper(key="timestamp", freq="1H")).agg("mean").index, 
                                               **train_test_split_kwargs)

    train_data = data[data["timestamp"].dt.floor(freq="H").isin(train_hours)].copy(deep=True)
    test_data = data[data["timestamp"].dt.floor(freq="H").isin(test_hours)].copy(deep=True)

    return train_data, test_data
