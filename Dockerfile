FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/scraped_data/linkedin

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9009

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9009", "--log-level", "info"]
