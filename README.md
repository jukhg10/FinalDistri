# Sistema Distribuido de Generación de Números Primos

Este proyecto implementa un sistema distribuido basado en microservicios sobre Kubernetes para la generación de números primos de gran tamaño (12+ dígitos). El sistema garantiza la unicidad de los números por solicitud y utiliza un algoritmo determinista "puro" (división por tentativa hasta la raíz cuadrada) para asegurar la primalidad al 100%.

## 📋 Arquitectura

El sistema sigue el patrón Productor-Consumidor:

1.  **API Gateway (FastAPI):** Recibe las solicitudes HTTP, genera un ID único y encola tareas individuales en Redis.
2.  **Cola de Mensajes (Redis):** Desacopla la recepción de solicitudes del procesamiento, permitiendo escalabilidad asíncrona.
3.  **Workers (Python):** Múltiples réplicas que consumen tareas de la cola. Cada worker:
    * Genera un candidato aleatorio impar.
    * Verifica en MongoDB que no exista previamente para esa solicitud (Unicidad).
    * Ejecuta el test de primalidad matemático (División por raíz cuadrada).
    * Guarda el resultado exitoso.
4.  **Base de Datos (MongoDB):** Persistencia de los números generados y estado del sistema.

## 🚀 Despliegue en Killercoda

### Prerrequisitos
- Acceso a un cluster de Kubernetes (ej. [Killercoda Playground](https://killercoda.com/playgrounds/scenario/kubernetes)).
- `kubectl` configurado.

### Instalación Rápida

1. **Clonar el repositorio:**
 
   git clone [https://github.com/jukhg10/FinalDistri.git](https://github.com/jukhg10/FinalDistri.git)
   cd FinalDistri
   
**2.Desplegar los servicios:**

  kubectl apply -f k8s/
  
3.**Verificar estado: Esperar a que todos los pods estén en estado Running:**
  kubectl get pods -w
  
****Guía de Uso****
**1. Solicitar nuevos números**
curl -X POST http://localhost:30000/new \
     -H "Content-Type: application/json" \
     -d '{"cantidad": 5, "digitos": 12}'; echo


**2. Consultar progreso** 
Reemplaza UUID con el ID recibido.

curl http://localhost:30000/status/UUID; echo

**3. Obtener resultados finales**
curl http://localhost:30000/result/UUID; echo
