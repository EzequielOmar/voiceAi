FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copy requirements.txt and install dependencies
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Upgrade pip and install TSS and requirements
#RUN pip install --upgrade pip
#RUN pip install TTS
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .
RUN mkdir -p /app/models

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "-u", "run.py"]
