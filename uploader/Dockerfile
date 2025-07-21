FROM python:3.11-slim

WORKDIR /app

COPY upload_server.py /app/upload_server.py

RUN pip install flask

EXPOSE 8080
CMD ["python", "upload_server.py"]
