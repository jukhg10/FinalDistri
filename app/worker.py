import redis
import os
import time
from pymongo import MongoClient
from logic import es_primo, generar_candidato_impar

# Configuración
redis_host = os.getenv("REDIS_HOST", "localhost")
mongo_host = os.getenv("MONGO_HOST", "localhost")

r = redis.Redis(host=redis_host, port=6379, db=0)
client = MongoClient(f"mongodb://{mongo_host}:27017/")
db = client["primos_db"]
collection = db["resultados"]

print("Worker iniciado, esperando tareas...")

while True:
    _, mensaje_bytes = r.blpop("cola_primos") 
    mensaje = mensaje_bytes.decode("utf-8")
    
    req_id, digitos_str = mensaje.split(":")
    digitos = int(digitos_str)
    
    encontrado = False
    while not encontrado:
        candidato = generar_candidato_impar(digitos)
        
        existe = collection.find_one({"req_id": req_id, "numero": candidato})
        if existe:
            continue 
            
        if es_primo(candidato):
            collection.insert_one({"req_id": req_id, "numero": candidato})
            print(f"Primo encontrado para {req_id}: {candidato}")
            encontrado = True
