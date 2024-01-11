from enum import Enum


class AvailableModels(str, Enum):
    base = "base"
    logreg_tfidf = "logreg_tfidf"
    catboost = "catboost"
