# Use an official slim Python image
FROM python:3.10-slim

# 1) Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg \
      fonts-dejavu-core \
      libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# 2) Set workdir
WORKDIR /app

# 3) Copy only requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# 4) Copy rest of the code
COPY . .

# 5) Default command
CMD ["python", "main.py"]
