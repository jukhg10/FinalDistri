from fastapi import FastAPI
from pydantic import BaseModel
import redis
import uuid
import os
from pymongo import MongoClient

app = FastAPI()

# Conexiones (Usaremos variables de entorno para K8s)
redis_host = os.getenv("REDIS_HOST", "localhost")
mongo_host = os.getenv("MONGO_HOST", "localhost")

r = redis.Redis(host=redis_host, port=6379, db=0)
client = MongoClient(f"mongodb://{mongo_host}:27017/")
db = client["primos_db"]
collection = db["resultados"]

class Solicitud(BaseModel):
    cantidad: int
    digitos: int

@app.post("/new") # [cite: 11]
def nueva_solicitud(solicitud: Solicitud):
    req_id = str(uuid.uuid4())
    
    # Encolar N tareas individuales en Redis
    for _ in range(solicitud.cantidad):
        # Formato del mensaje: ID_SOLICITUD:DIGITOS
        mensaje = f"{req_id}:{solicitud.digitos}"
        r.lpush("cola_primos", mensaje) # [cite: 25]
        
    return {"id": req_id}

@app.get("/status/{req_id}") # [cite: 15]
def consultar_status(req_id: str):
    # Contamos cuántos primos hay en la DB con ese ID
    count = collection.count_documents({"req_id": req_id})
    return {"id": req_id, "completados": count}

@app.get("/result/{req_id}") # [cite: 19]
def obtener_resultados(req_id: str):
    # Buscamos los números y ocultamos el _id de mongo
    cursor = collection.find({"req_id": req_id}, {"_id": 0, "numero": 1})
    numeros = [doc["numero"] for doc in cursor]
    return {"id": req_id, "numeros": numeros}