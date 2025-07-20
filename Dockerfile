# Use a slim Python 3.10 base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
