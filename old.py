import numpy as np
from sklearn.svm import SVC
import pickle

def main():
    model = get_model()
    accuracy = test_model(model)
    print(f"Accuracy: {accuracy:.2f}%")
        
def get_model():
    wants_to_train = prompt("Do you want to train the model (y/n)?")
    if wants_to_train == "y" or wants_to_train == "Y":
        training_data_path = prompt("Enter path to the training data file:")
        model = build_model(training_data_path)
        store_model(model)
        return model
    else:
        model_path = prompt("Enter path to the model file:")
        return load_model(model_path)
        

def build_model(path: str):
    raw_data = read_file(path)
    data = np.array(parse_data(raw_data))
    
    X, y = format_data(data)
    
    model = SVC()
    model.fit(X, y)
    
    return model

def store_model(model):
    path = prompt("Enter path at which to store the model:")
    
    with open(path, "wb") as file:
        pickle.dump(model, file)
        

def load_model(path: str):
    with open(path, 'rb') as file:
        return pickle.load(file)
        
def get_test_data(path: str):
    raw_data = read_file(path)
    return np.array(parse_data(raw_data))

def test_model(model):
    test_data_path = prompt("Enter path to the test data file:")
    test_data = get_test_data(test_data_path)
    
    X, y = format_data(test_data)
    
    y_pred = model.predict(X)
    accuracy = np.mean(y_pred == y) * 100
    
    return accuracy

def parse_data(data: str):
    return [[int(col) for col in row.split(",")] for row in data.splitlines()]

def format_data(data):
    X = data[:, :-1]
    y = data[:, -1:].flatten()
    return X, y

def prompt(message: str):
    print(message, end=" ")
    return input()

def read_file(path: str):
    with open(path, "r") as file:
        return file.read()

if __name__ == "__main__":
    main()