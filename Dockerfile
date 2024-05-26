# Use the official Python image as a base image
FROM python:3.9-slim

# Set the MongoDB connection string as an environment variable
ENV MONGODB_CONNECTION_STRING="mongodb+srv://adarsh:admin%40123@cluster0.03woj0o.mongodb.net/"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /app
COPY . .

# Expose port 4000 to the outside world
EXPOSE 4000

# Command to run the FastAPI server when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]
