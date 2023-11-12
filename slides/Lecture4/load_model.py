from dataclasses import dataclass
from sklearn import svm, ensemble

@dataclass
class ClassificationModel:
    model_name: str
    model_parameters: dict

    def create_model(self):
        if self.model_name == 'SVM':
            return svm.SVC(**self.model_parameters)
        elif self.model_name == 'RandomForest':
            return ensemble.RandomForestClassifier(**self.model_parameters)
        else:
            raise ValueError("Unknown model name: {}".format(self.model_name))

# Пример использования
model_data = {
    'model_name': 'RandomForest',
    'model_parameters': {'n_estimators': 100, 'max_depth': 5}
}

classification_model = ClassificationModel(**model_data)
classifier = classification_model.create_model()







from dataclasses import dataclass
from sklearn import svm, ensemble
import joblib


@dataclass
class ClassificationModel:
    model_name: str
    model_parameters: dict
    model_path: str

    def create_model(self):
        if self.model_name == 'SVM':
            model = svm.SVC(**self.model_parameters)
        elif self.model_name == 'RandomForest':
            model = ensemble.RandomForestClassifier(**self.model_parameters)
        else:
            raise ValueError("Unknown model name: {}".format(self.model_name))

        model.load(self.model_path)
        return model


# Пример использования
model_data = {
    'model_name': 'RandomForest',
    'model_parameters': {'n_estimators': 100, 'max_depth': 5},
    'model_path': 'model_weights.pkl'
}

classification_model = ClassificationModel(**model_data)
classifier = classification_model.create_model()
