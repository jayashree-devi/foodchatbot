# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for MariaDB support
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the entire Django project into the container
COPY . /app

# Copy environment file (ensure it exists in the directory)
COPY .env /app/

# Expose the port the app will run on
EXPOSE 8000

# Set the default command to run the Django development server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
