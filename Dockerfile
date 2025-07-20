FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY trading-bot/requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all code
COPY trading-bot .

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
