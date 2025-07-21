 #hm
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install dependencies system (agar psycopg2, motor, dll bisa di-compile)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc g++ libpq-dev python3-dev build-essential ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Salin semua file ke container
COPY . .

# Upgrade pip dan install dependencies Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Jalankan main.py
CMD ["python", "main.py"]
