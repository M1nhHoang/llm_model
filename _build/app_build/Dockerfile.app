FROM python:3.10-slim-buster

WORKDIR /app

COPY app/main.py .
COPY app/static .

RUN pip install fastapi uvicorn requests aiohttp

CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 80"]
