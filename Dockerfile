# Use the latest Python version (Python 3.13)
FROM python:3.13-slim


# Set the working directory inside the container
WORKDIR /app


# Copy the requirements file into the container
COPY requirements.txt .


# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]
