FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/todo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
