# SET BASE IMAGE OS
FROM python:3.9-alpine

# Update & install git
RUN apk update && apk add --no-cache git

# Set workdir dan copy file lokal ke container
WORKDIR /app
COPY . /app

# Supaya pip tidak warning
ENV PIP_ROOT_USER_ACTION=ignore

# Update pip dan install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Jalankan main.py
CMD ["python", "main.py"]
