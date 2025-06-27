import joblib
import json
from datetime import datetime

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

CONFIDENCE_THRESHOLD = config["confidence_threshold"]

# Load model & vectorizer from config
model = joblib.load(config["model_path"])
vectorizer = joblib.load(config["vectorizer_path"])

def predict_spam(text: str):
    vec = vectorizer.transform([text])
    proba = model.predict_proba(vec)[0]

    print("Model classes:", model.classes_)
    print("Prediction probabilities:", proba)

    # Determine spam index
    labels = config.get("labels", ["spam", "not_spam"])
    spam_label = labels[0]
    not_spam_label = labels[1]

    if spam_label in model.classes_:
        spam_index = list(model.classes_).index(spam_label)
    elif 1 in model.classes_:
        spam_index = list(model.classes_).index(1)
    else:
        raise ValueError("'spam' label not found in model classes")

    confidence = proba[spam_index]
    label = spam_label if confidence >= CONFIDENCE_THRESHOLD else not_spam_label

    # Logging
    if config.get("log_predictions", True):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"[{now}] Text: {text[:50]}... | Label: {label} | Confidence: {round(confidence, 2)}"
        print(log_text)
        with open("logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_text + "\n")

    return {
        "label": label,
        "confidence": round(confidence, 2)
    }
