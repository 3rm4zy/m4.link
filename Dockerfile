FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ templates/
COPY config.ini .
COPY entrypoint.py .
COPY app.py .

RUN mkdir -p html

EXPOSE 5000

CMD ["sh", "-c", "python entrypoint.py && gunicorn --bind 0.0.0.0:5000 app:app"]