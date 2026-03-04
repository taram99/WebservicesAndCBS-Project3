# syntax=docker/dockerfile:1 source docs.docker.com
#auth service
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir flask pyjwt requests
EXPOSE 8001
CMD ["python3", "app2.py"]
