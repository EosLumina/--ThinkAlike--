# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn for running FastAPI in production
RUN pip install gunicorn

# Copy only the necessary files for the backend
COPY backend /app/backend

# Copy only the necessary files for the frontend
COPY frontend /app/frontend

# Expose the port the app runs on
EXPOSE 8000

# Command to run the backend server
CMD ["gunicorn", "backend.app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
