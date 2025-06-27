# Step 1: Start from a lightweight Python image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy your entire project into the container
COPY . .

# Step 5: Set environment path for Python
ENV PYTHONPATH=/app

# Step 6: Expose port 8000 (FastAPI runs here)
EXPOSE 8000

# Step 7: Start the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
