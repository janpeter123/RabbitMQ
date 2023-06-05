# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the FastAPI application file
COPY . .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for RabbitMQ
ENV RABBITMQ_HOST=localhost

# Expose the port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
