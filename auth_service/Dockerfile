# syntax=docker/dockerfile:1 source docs.docker.com
#auth service
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8001
CMD ["python3", "app2.py"]
