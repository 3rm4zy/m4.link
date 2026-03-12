FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ templates/
COPY config.ini .
COPY entrypoint.py .
COPY app.py .


RUN useradd -m -u 1000 appuser
RUN mkdir -p html && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["sh", "-c", "python entrypoint.py && gunicorn --bind 0.0.0.0:5000 app:app"]