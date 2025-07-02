# Use a base Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (match your app.py default or Railway's 8080)
EXPOSE 8080

# Start the app using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
