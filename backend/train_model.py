import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error


# ==========================
# Load Dataset
# ==========================
dataset_path = r"C:\Users\arthi\OneDrive\Pictures\Desktop\diamondprice\backend\templates\data\diamonds.csv"

df = pd.read_csv(dataset_path)

# Remove unnecessary column if present
if "Unnamed: 0" in df.columns:
    df.drop(columns=["Unnamed: 0"], inplace=True)


# ==========================
# Encode Categorical Columns
# ==========================
categorical_columns = ["cut", "color", "clarity"]

encoders = {}

for column in categorical_columns:
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column])
    encoders[column] = encoder


# ==========================
# Features & Target
# ==========================
X = df.drop("price", axis=1)
y = df["price"]


# ==========================
# Train-Test Split
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ==========================
# Train Model
# ==========================
model = RandomForestRegressor(
    n_estimators=30,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ==========================
# Model Evaluation
# ==========================
predictions = model.predict(X_test)

r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print("=" * 40)
print("Model Performance")
print("=" * 40)
print(f"R² Score : {r2:.4f}")
print(f"MAE      : {mae:.2f}")
print("=" * 40)


# ==========================
# Save Model
# ==========================
model_data = {
    "model": model,
    "encoders": encoders,
    "columns": list(X.columns)
}

model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(model_path, "wb") as file:
    pickle.dump(model_data, file)

print(f"\nModel saved successfully!")
print(f"Location: {model_path}")