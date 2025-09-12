# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Upgrade pip
RUN pip install --upgrade pip

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the dependencies file to the working directory
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl postgresql-client

# Copy the rest of the application's code to the working directory
COPY . .

# Copy debugpy script
COPY utils/vsdebugpy.sh /usr/bin/vsdebugpy
RUN chmod +x /usr/bin/vsdebugpy

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
