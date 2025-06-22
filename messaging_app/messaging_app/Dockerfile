# Use Python 3.10 as base image
# This tells Docker to start with a pre-built Python 3.10 image
FROM python:3.10

# Set environment variables
# PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files
# PYTHONUNBUFFERED=1 ensures Python output is sent straight to terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
# This creates a directory called /app inside the container and makes it the working directory
WORKDIR /app

# Install system dependencies
# Updates package list and installs PostgreSQL client (common for Django apps)
# Cleans up afterward to keep image size small
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
# This copies your requirements.txt file from your local machine to the container
COPY requirements.txt /app/

# Install Python dependencies
# Upgrades pip and installs all packages listed in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
# This copies ALL your project files from your local machine to the container
COPY . /app/

# Create a non-root user (security best practice)
# Creates a user called 'appuser' and gives them ownership of the /app directory
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
# Tells Docker that the container will use port 8000
EXPOSE 8000

# Command to run the application
# This is the command that runs when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]