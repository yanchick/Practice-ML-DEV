from abc import ABC, abstractmethod
from pathlib import Path
import pickle

import pandas as pd

class AbstractModel(ABC):
    __instance = None

    @abstractmethod
    def fit(self, *args, **kwargs) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def predict(self, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError
    
    def save(self, filename: Path) -> None:
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filename: Path) -> 'AbstractModel':
        if cls.__instance is None:
            with open(filename, "rb") as file:
                cls.__instance = pickle.load(file)

        return cls.__instance
