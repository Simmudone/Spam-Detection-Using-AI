# app/main.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from app.generator import predict_spam
import json

# Load version info from config
with open("config.json", "r") as f:
    config = json.load(f)

app = FastAPI(title="Spam Detection Microservice")

# Define input model
class PostInput(BaseModel):
    post: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def version_info():
    return {
        "model_name": config.get("model_name"),
        "version": config.get("version")
    }

@app.post("/predict")
def predict(post_input: PostInput):
    if not post_input.post.strip():
        raise HTTPException(status_code=400, detail="Post content is empty")
    return predict_spam(post_input.post)
