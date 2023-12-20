from data_preprocessing import load_and_process_data
from ml_models import train_and_evaluate_models

def main():
    X_train_scaled, X_test_scaled, y_train, y_test = load_and_process_data()
    model = train_and_evaluate_models(X_train_scaled, X_test_scaled, y_train, y_test)

if __name__ == "__main__":
    main()
    