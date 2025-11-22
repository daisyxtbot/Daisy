# ---- Base Image ----
FROM python:3.11-alpine

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Work directory ----
WORKDIR /app

# ---- Copy requirements ----
COPY requirements.txt .

# ---- Install Python dependencies ----
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---- Copy project ----
COPY . .

# ---- Start ----
CMD ["python3", "Rosie"]    