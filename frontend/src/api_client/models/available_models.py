from enum import Enum


class AvailableModels(str, Enum):
    BASE = "base"
    CATBOOST = "catboost"
    LOGREG_TFIDF = "logreg_tfidf"

    def __str__(self) -> str:
        return str(self.value)
