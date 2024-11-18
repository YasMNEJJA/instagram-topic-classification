# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
