"""
Heart Disease Model Training Script
Dataset: UCI Cleveland Heart Disease Dataset (fetched from UCI ML Repository)
"""

import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("=" * 50)
print("Heart Disease Model Training")
print("=" * 50)

# ── 1. Load Dataset ──────────────────────────────────
# UCI Cleveland Heart Disease dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

columns = [
    'age', 'sex', 'cp', 'trestbps', 'chol',
    'fbs', 'restecg', 'thalach', 'exang',
    'oldpeak', 'slope', 'ca', 'thal', 'target'
]

print("\n[1] Loading dataset from UCI repository...")
try:
    import ssl
    import urllib.request
    import io
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(url, context=ctx) as response:
        raw = response.read().decode('utf-8')
    df = pd.read_csv(io.StringIO(raw), names=columns, na_values='?')
    print(f"    Loaded {len(df)} rows")
except Exception as e:
    print(f"    Failed to fetch online: {e}")
    print("    Trying fallback local path...")
    df = pd.read_csv('heart.csv', names=columns, na_values='?')

# ── 2. Preprocess ────────────────────────────────────
print("\n[2] Preprocessing...")

# Drop rows with missing values
df.dropna(inplace=True)
print(f"    Rows after dropping NaN: {len(df)}")

# UCI target: 0 = no disease, 1-4 = disease present
# Convert to binary: 0 = not suffering, 1 = suffering
df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)

print(f"    Class distribution:\n{df['target'].value_counts().to_string()}")
print(f"    0 = Not Suffering, 1 = Suffering")

# ── 3. Features & Target ─────────────────────────────
X = df.drop('target', axis=1)
y = df['target']

print(f"\n[3] Features shape: {X.shape}")

# ── 4. Train/Test Split ──────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n[4] Train size: {len(X_train)}, Test size: {len(X_test)}")

# ── 5. Train Model ───────────────────────────────────
print("\n[5] Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# ── 6. Evaluate ──────────────────────────────────────
print("\n[6] Evaluation:")
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"    Test Accuracy: {acc * 100:.2f}%")

cv_scores = cross_val_score(model, X, y, cv=5)
print(f"    5-Fold CV Accuracy: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)")

print("\n    Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Not Suffering', 'Suffering']))

print("    Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"    [[TN={cm[0][0]}, FP={cm[0][1]}],")
print(f"     [FN={cm[1][0]}, TP={cm[1][1]}]]")

# ── 7. Verify label correctness ──────────────────────
print("\n[7] Sanity checks:")

# High risk: older male, chest pain, high cholesterol
hr = model.predict([[63, 1, 1, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]])
print(f"    High risk male (63yr, cp=1, chol=233): {hr[0]} -> {'SUFFERING ✓' if hr[0]==1 else 'NOT SUFFERING ✗'}")

# Low risk: young female, normal values
lr = model.predict([[45, 0, 2, 110, 200, 0, 1, 165, 0, 0.0, 2, 0, 2]])
print(f"    Low risk female (45yr, normal vals):   {lr[0]} -> {'NOT SUFFERING ✓' if lr[0]==0 else 'SUFFERING ✗'}")

# ── 8. Save Model ────────────────────────────────────
print("\n[8] Saving model as heart_disease.pkl ...")
joblib.dump(model, 'heart_disease.pkl')
print("    Saved successfully!")
print("\n" + "=" * 50)
print("Training complete.")
print("=" * 50)
