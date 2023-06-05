# Use a Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY . .


RUN pip install --no-cache-dir -r requirements.txt


# Run the Python script when the container starts
CMD ["python", "main.py"]
