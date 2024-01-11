from enum import Enum


class AvailableModels(str, Enum):
    naive = "naive"
    linear = "linear"
    tree = "tree"
    dummy = "dummy"
