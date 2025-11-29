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
    # 1. Leer de la cola (Bloqueante, espera 0 indefinidamente hasta que llegue algo)
    # blpop retorna una tupla (cola, mensaje)
    _, mensaje_bytes = r.blpop("cola_primos") 
    mensaje = mensaje_bytes.decode("utf-8")
    
    # 2. Parsear el mensaje
    req_id, digitos_str = mensaje.split(":")
    digitos = int(digitos_str)
    
    encontrado = False
    while not encontrado:
        # A. Generar candidato
        candidato = generar_candidato_impar(digitos)
        
        # B. Verificar unicidad en la BD para esa solicitud [cite: 28]
        existe = collection.find_one({"req_id": req_id, "numero": candidato})
        if existe:
            continue # Si ya existe, probamos otro número
            
        # C. Test de primalidad (Pesado)
        if es_primo(candidato):
            # Guardar en DB
            collection.insert_one({"req_id": req_id, "numero": candidato})
            print(f"Primo encontrado para {req_id}: {candidato}")
            encontrado = True
            # Al salir del bucle while, el worker vuelve al inicio a pedir otro trabajo a Redis