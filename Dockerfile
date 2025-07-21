# SET BASE IMAGE OS
FROM python:3.9-alpine

# Update & install git
RUN apk update && apk add --no-cache git

# Clone repo kamu
RUN git clone https://github.com/temankuya/subia /app

# Set workdir ke folder project
WORKDIR /app

# Optional: Set git config (bisa dihapus kalau tidak perlu)
RUN git config --global user.name "subia"
RUN git config --global user.email "subia@e.mail"

# Supaya pip tidak warning
ENV PIP_ROOT_USER_ACTION=ignore

# Update pip dan install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Jalankan main.py (pastikan ini file utama)
CMD ["python", "main.py"]
