# ---- Base Image ----
FROM python:3.11-slim

# ---- Prevent python from writing .pyc files ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Set work directory ----
WORKDIR /app

# ---- Update system & install dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# ---- Upgrade pip ----
RUN pip install --upgrade pip

# ---- Copy requirements ----
COPY requirements.txt .

# ---- Install requirements ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Start command ----
CMD ["python3", "Rosie"]