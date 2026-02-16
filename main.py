import pickle
import numpy as np
from sklearn.svm import SVC
from abc import ABC, abstractmethod

# interface just in case I end up building my own model before submitting
class Model(ABC):
    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray):
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        pass


class DigitClassifier:
    def __init__(self, model: Model):
        self.model = model

    def train(self, path: str):
        X, y = self._load_data(path)
        self.model.fit(X, y)

    def test(self, path: str) -> float:
        X, y = self._load_data(path)
        predictions = self.model.predict(X)
        
        for i in range(len(X)):
            print(f"{''.join(map(str, X[i]))} | {y[i]} -> {predictions[i]}")
        
        return np.mean(predictions == y) * 100

    def persist(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            self.model = pickle.load(f)

    @staticmethod
    def _load_data(path: str):
        with open(path, "r") as f:
            rows = [[int(col) for col in line.split(",")] for line in f if line.strip()]
        data = np.array(rows)
        return data[:, :-1], data[:, -1]


def main():
    classifier = DigitClassifier(SVC())

    wants_to_train = prompt("Do you want to train the model (y/n)?")
    if wants_to_train.lower() == "y":
        training_data_path = prompt("Enter path to the training data file:")
        classifier.train(training_data_path)
        model_storage_path = prompt("Enter path at which to store the model:")
        classifier.persist(model_storage_path)
    else:
        model_path = prompt("Enter path to the model file:")
        classifier.load(model_path)

    test_data_path = prompt("Enter path to the test data file:")
    accuracy = classifier.test(test_data_path)
    print(f"Accuracy: {accuracy:.4f}%")


def prompt(message: str):
    print(message, end=" ")
    return input()

if __name__ == "__main__":
    main()
