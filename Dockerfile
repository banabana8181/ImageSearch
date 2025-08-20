# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Cloud Run sets $PORT automatically
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
