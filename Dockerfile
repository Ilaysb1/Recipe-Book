# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . /app

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory


# Expose the port that the Flask app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "main.py"]

