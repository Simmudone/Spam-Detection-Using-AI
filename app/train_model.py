import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# Load cleaned dataset
data_path = "data/cleaned_dataset.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError("cleaned_dataset.csv not found. Please run cleaning script.")
#df = pd.read_csv(data_path)
df = pd.read_csv("data/cleaned_dataset.csv")  # use the cleaned file

# Features and labels
#X = df['clean_text']
X = df['clean_text'].fillna("")
y = df['label']

# TF-IDF vectorization
#vectorizer = TfidfVectorizer()
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=3000)
X_vec = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Model training
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("=== Evaluation Metrics ===")
print(f"Accuracy: {accuracy:.2f}")
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", report)

# Save model and vectorizer
os.makedirs("app/model", exist_ok=True)
joblib.dump(model, "app/model/model.pkl")
joblib.dump(vectorizer, "app/model/vectorizer.pkl")
print("\n✅ Model and vectorizer saved to 'app/model/'")