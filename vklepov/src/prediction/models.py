from dataclasses import dataclass


@dataclass
class PredictionModel:
    name: str
    description: str
    id: str
    cost: int


model_list = [
    PredictionModel(
        name="Basic Protection",
        description="A simple yet effective malware detector for basic security",
        cost=10000,
        id="logistic-regression",
    ),
    PredictionModel(
        name="Premium Safery Deluxe",
        description="State-of-the art malware detector for sensitive applications",
        cost=30000,
        id="random-forest",
    ),
]

models = dict((m.id, m) for m in model_list)
