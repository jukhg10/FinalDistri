# Sistema Distribuido de Generación de Números Primos

> **¿Qué hace este programa?**  
> Este proyecto implementa un sistema distribuido basado en microservicios sobre Kubernetes para la generación de números primos de gran tamaño (12+ dígitos). El sistema garantiza la unicidad de los números por solicitud y utiliza un algoritmo determinista "puro" (división por tentativa hasta la raíz cuadrada) para asegurar la primalidad al 100%.

---

## Índice

1. [¿Cómo funciona el sistema? (Versión simple)](#cómo-funciona-el-sistema-versión-simple)
2. [Arquitectura técnica](#arquitectura-técnica)
3. [Guía paso a paso para usar el sistema](#guía-paso-a-paso-para-usar-el-sistema)
4. [Guía de uso de la API](#guía-de-uso-de-la-api)
5. [Solución de problemas](#solución-de-problemas)
6. [Preguntas frecuentes](#preguntas-frecuentes)

---

##  ¿Cómo funciona el sistema? (Versión simple)

Imagina que tienes una **fábrica de números primos**:

```
┌─────────────┐      ┌──────────┐      ┌────────────┐      ┌──────────┐
│ Tú envías   │ -->  │  Cola de │ -->  │ 3 Workers  │ -->  │ Base de  │
│ solicitud   │      │  tareas  │      │ (trabajan  │      │  datos   │
│ (API)       │      │ (Redis)  │      │  paralelo) │      │ (MongoDB)│
└─────────────┘      └──────────┘      └────────────┘      └──────────┘
```

### Paso a paso:

1. **Tú haces una solicitud** → "Quiero 5 números primos de 12 dígitos"
2. **El sistema crea 5 tareas** → Cada tarea = "Encuentra 1 número primo"
3. **3 trabajadores (workers) compiten** → Toman tareas y buscan números primos
4. **Se guardan en la base de datos** → Los resultados quedan almacenados
5. **Tú consultas los resultados** → Cuando todo esté listo, obtienes tus 5 números

### ¿Por qué es rápido?

En lugar de tener **1 persona** buscando 5 números (lento), tienes **3 personas** trabajando al mismo tiempo. Si aumentas a 10 workers, ¡será aún más rápido!

---

##  Arquitectura técnica

> **Para usuarios técnicos**: El sistema sigue el patrón **Productor-Consumidor** con microservicios en Kubernetes.

### Componentes:

1. **API Gateway (FastAPI)**
   - Recibe solicitudes HTTP
   - Genera un ID único por solicitud
   - Encola tareas individuales en Redis

2. **Cola de Mensajes (Redis)**
   - Desacopla recepción de procesamiento
   - Permite escalabilidad horizontal

3. **Workers (Python) - 3 réplicas**
   - Generan candidatos aleatorios impares
   - Verifican unicidad en MongoDB
   - Ejecutan test de primalidad (división hasta √n)
   - Persisten resultados exitosos

4. **Base de Datos (MongoDB)**
   - Almacena números primos generados
   - Garantiza unicidad por ID de solicitud

### Algoritmo:
- **Test de primalidad "puro"**: División por tentativa hasta la raíz cuadrada
- **Garantía matemática**: 100% de certeza (no probabilístico)

---

##  Guía paso a paso para usar el sistema

### **Opción A: Usar en la nube (Killercoda - GRATIS)**

> **Recomendado para principiantes**: No necesitas instalar nada en tu computadora.

#### **PASO 1: Acceder al entorno de Kubernetes**

1. Abre tu navegador y ve a: **[Killercoda Kubernetes Playground](https://killercoda.com/playgrounds/scenario/kubernetes)**
2. Espera 30-60 segundos a que cargue el entorno
3. Verás una **terminal negra** en tu navegador ← Aquí ejecutarás los comandos

#### **PASO 2: Descargar el código**

Copia y pega este comando en la terminal:

```bash
git clone https://github.com/jukhg10/FinalDistri.git
cd FinalDistri
```

**¿Qué hace esto?**
- Descarga el código del proyecto desde GitHub
- Entra en la carpeta del proyecto

#### **PASO 3: Iniciar todos los servicios**

Copia y pega:

```bash
kubectl apply -f k8s/
```

**¿Qué hace esto?**
- Inicia la base de datos (MongoDB)
- Inicia la cola de mensajes (Redis)
- Inicia el servidor API
- Inicia 3 workers

#### **PASO 4: Verificar que todo esté funcionando**

Copia y pega:

```bash
kubectl get pods -w
```

**Espera hasta ver algo como esto:**

```
NAME                          READY   STATUS    
api-server-xxxxx              1/1     Running   
mongo-xxxxx                   1/1     Running   
redis-xxxxx                   1/1     Running   
worker-primos-xxxxx           1/1     Running   
worker-primos-yyyyy           1/1     Running   
worker-primos-zzzzz           1/1     Running   
```

Cuando todos digan **"Running"**, presiona `Ctrl+C` para salir.

---

### **Opción B: Usar en tu computadora (Requiere instalaciones)**

#### **Prerrequisitos:**
- Docker Desktop instalado
- Kubernetes habilitado en Docker Desktop
- Terminal (CMD, PowerShell o Git Bash)

#### **Pasos:**

```bash
# 1. Clonar repositorio
git clone https://github.com/jukhg10/FinalDistri.git
cd FinalDistri

# 2. Desplegar servicios
kubectl apply -f k8s/

# 3. Verificar estado
kubectl get pods -w
```

---

##  Guía de uso de la API

Una vez que el sistema esté corriendo, puedes usarlo haciendo **peticiones HTTP**. Aquí te explicamos cómo:

---

### ** ACCIÓN 1: Solicitar números primos**

#### **Comando:**

```bash
curl -X POST http://localhost:30000/new \
     -H "Content-Type: application/json" \
     -d '{"cantidad": 5, "digitos": 12}'; echo
```

#### **Explicación de los parámetros:**

- `"cantidad": 5` → Cuántos números primos quieres (en este caso, 5)
- `"digitos": 12` → De cuántos dígitos (en este caso, 12 dígitos)

#### **Respuesta que recibirás:**

```json
{"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}
```

> **IMPORTANTE**: Copia ese `id`, lo necesitarás para los siguientes pasos.

#### **¿Qué pasó?**
El sistema creó 5 tareas y las puso en la cola. Los 3 workers están ahora buscando números primos.

---

### ** ACCIÓN 2: Consultar el progreso**

#### **Comando:**

Reemplaza `TU_ID_AQUI` con el ID que recibiste en el paso anterior:

```bash
curl http://localhost:30000/status/TU_ID_AQUI; echo
```

#### **Ejemplo real:**

```bash
curl http://localhost:30000/status/a1b2c3d4-e5f6-7890-abcd-ef1234567890; echo
```

#### **Respuesta:**

```json
{"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "completados": 3}
```

**Interpretación:**
- `"completados": 3` → Ya se encontraron 3 de los 5 números primos solicitados
- Puedes ejecutar este comando varias veces hasta que `completados` sea igual a 5

---

### ** ACCIÓN 3: Obtener los resultados finales**

#### **Comando:**

```bash
curl http://localhost:30000/result/TU_ID_AQUI; echo
```

#### **Ejemplo real:**

```bash
curl http://localhost:30000/result/a1b2c3d4-e5f6-7890-abcd-ef1234567890; echo
```

#### **Respuesta:**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "numeros": [
    123456789011,
    987654321019,
    555555555557,
    777777777773,
    999999999989
  ]
}
```

**Listo!** Estos son tus 5 números primos de 12 dígitos.

---

### ** Ejemplo completo de uso:**

```bash
# 1. Solicitar 10 números primos de 15 dígitos
curl -X POST http://localhost:30000/new \
     -H "Content-Type: application/json" \
     -d '{"cantidad": 10, "digitos": 15}'; echo

# Respuesta: {"id": "xyz-123-abc"}

# 2. Consultar progreso (ejecutar varias veces)
curl http://localhost:30000/status/xyz-123-abc; echo

# Respuesta: {"id": "xyz-123-abc", "completados": 7}
# (Espera unos segundos y vuelve a consultar)

# 3. Obtener resultados cuando esté completo
curl http://localhost:30000/result/xyz-123-abc; echo
```

---

##  Solución de problemas

### **Problema: "Connection refused" o "No se puede conectar"**

**Solución:**

1. Verifica que los pods estén corriendo:
   ```bash
   kubectl get pods
   ```
   
2. Si algún pod está en estado `Pending` o `Error`, espera 1-2 minutos y vuelve a verificar.

3. Si persiste, reinicia el despliegue:
   ```bash
   kubectl delete -f k8s/
   kubectl apply -f k8s/
   ```

---

### **Problema: "Los resultados tardan mucho"**

**Explicación:** Encontrar números primos grandes es computacionalmente costoso.

**Solución: Aumentar workers**

1. Edita el archivo `k8s/03-worker.yaml`
2. Cambia `replicas: 3` por `replicas: 10`
3. Aplica los cambios:
   ```bash
   kubectl apply -f k8s/03-worker.yaml
   ```

---

### **Problema: "El comando kubectl no se encuentra"**

**Solución en Killercoda:** Ya viene instalado, asegúrate de estar en el playground correcto.

**Solución en Windows:**
1. Instala [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. En Docker Desktop, ve a Settings → Kubernetes → Enable Kubernetes

---

##  Preguntas frecuentes

### **1. ¿Por qué usar sistemas distribuidos?**

**Velocidad**: Con 3 workers, el proceso es ~3 veces más rápido. Con 10 workers, ~10 veces más rápido.

**Analogía:** Es como tener 10 cajeros en un banco en lugar de 1. Las filas se mueven mucho más rápido.

---

### **2. ¿Puedo cambiar el número de dígitos?**

Sí, puedes solicitar números primos de **cualquier tamaño**:

```bash
# Números de 8 dígitos (más rápido)
curl -X POST http://localhost:30000/new \
     -H "Content-Type: application/json" \
     -d '{"cantidad": 20, "digitos": 8}'; echo

# Números de 20 dígitos (más lento)
curl -X POST http://localhost:30000/new \
     -H "Content-Type: application/json" \
     -d '{"cantidad": 5, "digitos": 20}'; echo
```

---

### **3. ¿Cómo detengo el sistema?**

```bash
kubectl delete -f k8s/
```

Esto detiene y elimina todos los servicios.

---

### **4. ¿Los números son realmente primos al 100%?**

**Sí**. El sistema usa un algoritmo matemático determinista (división hasta la raíz cuadrada) que **garantiza** que el número es primo. No es probabilístico.

---

### **5. ¿Puedo hacer múltiples solicitudes al mismo tiempo?**

Sí! Cada solicitud recibe un ID único. Puedes tener 10 solicitudes diferentes procesándose simultáneamente.

```bash
# Solicitud 1
curl -X POST http://localhost:30000/new -H "Content-Type: application/json" -d '{"cantidad": 5, "digitos": 12}'; echo

# Solicitud 2 (inmediatamente después)
curl -X POST http://localhost:30000/new -H "Content-Type: application/json" -d '{"cantidad": 3, "digitos": 15}'; echo
```

Cada una tendrá su propio ID y se procesarán en paralelo.

---

### **6. ¿Qué tecnologías usa el sistema?**

| Tecnología | ¿Para qué sirve? |
|------------|------------------|
| **Kubernetes** | Orquestador que gestiona los contenedores |
| **Docker** | Empaqueta el código para que corra en cualquier lugar |
| **FastAPI** | Framework Python para crear la API web |
| **Redis** | Base de datos en memoria que funciona como cola |
| **MongoDB** | Base de datos que guarda los resultados |
| **Python** | Lenguaje de programación |



##  Soporte

Si tienes problemas:

1. **Revisa la sección [Solución de problemas](#-solución-de-problemas)**
2. **Abre un Issue** en GitHub: [https://github.com/jukhg10/FinalDistri/issues](https://github.com/jukhg10/FinalDistri/issues)
3. **Verifica los logs** de los pods:
   ```bash
   kubectl logs -l app=worker
   ```

---

##  Conceptos clave explicados

### **¿Qué es Kubernetes?**
Es como un "director de orquesta" que gestiona múltiples contenedores (mini-computadoras virtuales). Se asegura de que todo esté corriendo y se reinicia automáticamente si algo falla.

### **¿Qué es una API?**
Es como el "menú de un restaurante". Le dices qué quieres (números primos), y te lo sirven. La comunicación se hace mediante URLs (`http://localhost:30000/new`).

### **¿Qué es Redis?**
Es una base de datos ultra-rápida que usamos como "lista de tareas pendientes". Los workers toman tareas de ahí.

### **¿Qué es MongoDB?**
Es una base de datos donde guardamos los resultados finales (los números primos encontrados).

