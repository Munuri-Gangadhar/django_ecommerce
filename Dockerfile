# Use the official Python slim image
FROM python:3.11.4-slim-bullseye

# Set environment variables
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

# Copy requirements.txt and install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app

# Ensure the PYTHONPATH includes the project directory
ENV PYTHONPATH="/app"

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# Run database migrations (optional)
RUN python manage.py migrate

# Specify the WSGI entry point
CMD ["gunicorn", "ecom.wsgi:application", "--bind", "0.0.0.0:8000"]
