import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Load dataset
df = pd.read_csv("dataset/train.csv")

# Selected Features
features = [
    "GrLivArea",
    "OverallQual",
    "BedroomAbvGr",
    "FullBath",
    "GarageCars",
    "YearBuilt"
]

X = df[features]
y = df["SalePrice"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
predictions = model.predict(X_test)

score = r2_score(y_test, predictions)

print(f"Accuracy (R² Score): {score:.4f}")

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/house_model.pkl")
joblib.dump(score, "models/accuracy.pkl")

print("Model Saved Successfully")