# Use the official Python slim image
FROM python:3.11.4-slim-bullseye

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt into the container
COPY ./requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . /app

# Set the entrypoint
ENTRYPOINT ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
