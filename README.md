# Spam Detection Microservice (Indian + Hinglish Context)

This is a lightweight and production-ready spam detection microservice built with **FastAPI**, trained on a dataset containing **Indian content**, **Hinglish**, **WhatsApp-style text**, and **scam messages in INR**.

---

## 🎯 Features

- Detects spam messages using TF-IDF + Naive Bayes
- Preprocessing: emoji removal, stopword filtering, punctuation cleanup
- Hinglish and Indian financial slang awareness
- REST API with `/predict`, `/health`, and `/version`
- Logs every prediction in `logs.txt`
- Schema validation using `schema.json`
- Fully Dockerized and testable with `pytest`

---

## 📁 Project Structure

```
spam-detector/
├── app/
│   ├── main.py               # FastAPI app
│   ├── generator.py          # Loads model & predicts
│   ├── train_model.py        # Model training logic
│   └── data_cleaner.py       # Text preprocessing
│   └── model/
│       ├── model.pkl         # Trained model
│       └── vectorizer.pkl    # TF-IDF vectorizer
├── data/
│   ├── dataset.csv           # Raw dataset
│   └── cleaned_dataset.csv   # Cleaned text dataset
├── config.json               # App settings and file paths
├── schema.json               # JSON schema for output
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker container file
├── logs.txt                  # Prediction logs
├── tests/
│   ├── test_predict.py
│   ├── test_edge_cases.py
│   └── test_validation.py
├── README.md                 # This file
```

---

## 🔧 Setup & Execution Steps

### 🧼 1. Clean the Dataset

```bash
python app/data_cleaner.py
```

➡️ This will create: `data/cleaned_dataset.csv`

---

### 🧠 2. Train the Model

```bash
python app/train_model.py
```

➡️ Generates:
- `app/model/model.pkl`
- `app/model/vectorizer.pkl`

---

### 🚀 3. Run the FastAPI App

#### Install dependencies:

```bash
pip install -r requirements.txt
```

#### Start FastAPI:

```bash
uvicorn app.main:app --reload
```

➡️ Then visit:

- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/health
- http://localhost:8000/version

---

### 💬 Example Prediction

**POST /predict**
```json
{
  "post": "Get ₹1000 free recharge now!"
}
```

✅ Expected output:
```json
{
  "label": "spam",
  "confidence": 0.91
}
```

---

## 🐳 Docker Instructions

### Build the image:

```bash
docker build -t spam-detector .
```

### Run the container:

```bash
docker run -p 8000:8000 spam-detector
```

#### To mount local logs:

```bash
docker run -p 8000:8000 -v ${PWD}/logs.txt:/app/logs.txt spam-detector
```

---

## ✅ Run All Tests 

### 🧪 Option 1: Run tests manually
```bash
python tests/test_predict.py
python tests/test_edge_cases.py
python tests/test_validation.py
```

### 🧪 Option 2: Run all with pytest
```bash
pytest tests/ --disable-warnings -v
```

These tests check:
- Schema validation (`schema.json`)
- Prediction accuracy for spam input
- Response time < 1 second
- Health and version endpoints
- Edge cases (empty input, emojis, long texts)

---

## ⚙️ config.json Example

```json
{
  "model_name": "tfidf_nb_spam",
  "version": "1.0.0",
  "confidence_threshold": 0.6,
  "labels": ["spam", "not_spam"],
  "log_predictions": true,
  "model_path": "app/model/model.pkl",
  "vectorizer_path": "app/model/vectorizer.pkl"
}
```

---

## 📐 schema.json Structure

```json
{
  "type": "object",
  "properties": {
    "label": {
      "type": "string",
      "enum": ["spam", "not_spam"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0
    }
  },
  "required": ["label", "confidence"],
  "additionalProperties": false
}
```

---

## 👨‍💻 Author & Submission

**Intern:** Simhadri Done  
**Internship:** Turtil.ai, Summer 2025  
**Mentor:** Raj Shanmugam
