# Use the official Python image as a base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the ports used by the application
EXPOSE 5800 5801

# Grant access to video devices
RUN apt-get update && apt-get install -y v4l-utils

# Command to run the application using Waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5800", "app:app"]
