FROM python:3.11.7-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y sqlite3 && \
    apt-get clean

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


CMD ["sh", "-c", "python src/dataenrichment.py && tail -f /dev/null"]