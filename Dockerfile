FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Por defecto no ejecutamos nada, lo definimos en Kubernetes
CMD ["echo", "Define el comando en k8s"]