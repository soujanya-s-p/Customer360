# src/models/churn_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

features = pd.read_csv("data/gold/customer_360_features.csv")

# --- Simulate realistic churn with noise
features['churn'] = (features['recency'] > 180).astype(int)
features['churn'] = features['churn'].apply(lambda x: x if np.random.rand()>0.3 else 1-x)  # 30% noise

# --- Features & target
X = features.drop(columns=['customer_id', 'churn'])
y = features['churn']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'src/models/churn_model.pkl')
print("Churn model saved ✔️")
