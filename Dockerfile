FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requiements.txt
EXPOSE 5003
CMD ["python","app.py"]