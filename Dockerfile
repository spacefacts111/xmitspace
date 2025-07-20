# Use an official slim Python image
FROM python:3.10-slim

# Install ffmpeg (and font packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg \
      fonts-dejavu-core \
      libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "main.py"]
