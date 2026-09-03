# Budget Buddy container image

FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements-test.txt .
RUN python -m pip install --no-cache-dir -r requirements-test.txt

COPY . .

CMD ["python", "main.py"]
