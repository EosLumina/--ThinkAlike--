import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def retrain_model(data_file, model_file):
    # Load new data
    import pandas as pd
    data = pd.read_csv(data_file)  # Load data from `data_file`
    X, y = data.iloc[:, :-1], data.iloc[:, -1]  # Assuming last column is labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Retrain model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save updated model
    joblib.dump(model, model_file)
    print(f"Model retrained and saved to {model_file}")

if __name__ == "__main__":
    retrain_model("user_feedback_data.csv", "matching_model.pkl")
