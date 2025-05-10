# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application dependencies requirements file to the container
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Set environment variables (optional, but good practice)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production # Change to 'development' for debugging

# Define the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]