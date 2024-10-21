# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV OPENAI_KEY=sk-proj-hGXlwutMJ5LE4OOPIVXkE9X5eg2PX967Zc-VxRrO79rgUsXC1qAf81sq7syv8lBUpkozV46oYNT3BlbkFJBBZKwwqHH7BObtcWdkAn2fN0mZE8b2jN

# Run app.py when the container launches
CMD ["python", "main.py"]]