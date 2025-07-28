# Use a lightweight base image with Python 3
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Install system dependencies for PDF handling (PyMuPDF)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Expose any ports if needed (optional)
# EXPOSE 8080

# Command to run the script
CMD ["python", "main.py"]
