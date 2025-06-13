# ECS Monitoring API

Esta API permite consultar métricas, logs y servicios de clústeres ECS de AWS de manera sencilla utilizando FastAPI.

## Endpoints

### 1. Obtener Métricas de un Servicio

`GET /metrics`

**Parámetros:**
- `cluster` (str, obligatorio): Nombre del clúster ECS.
- `service` (str, obligatorio): Nombre del servicio ECS.

**Ejemplo de uso:**
```
GET /metrics?cluster=ECS-TRV-LOGIN-DEV&service=mi-servicio
```

---

### 2. Obtener Logs de un LogGroup

`GET /logs`

**Parámetros:**
- `logGroup` (str, obligatorio): Nombre del Log Group en CloudWatch.
- `minutos` (int, opcional, default=5, rango 1-60): Minutos hacia atrás para buscar logs.
- `limiteStreams` (int, opcional, default=5, rango 2-20): Número máximo de log streams a consultar.
- `filtro` (str, opcional): Texto para filtrar mensajes de log.

**Ejemplo de uso:**
```
GET /logs?logGroup=mi-log-group&minutos=10&limiteStreams=5&filtro=ERROR
```

---

### 3. Listar Servicios de un Clúster ECS

`GET /services`

**Parámetros:**
- `cluster` (str, obligatorio): Nombre del clúster ECS.

**Ejemplo de uso:**
```
GET /services?cluster=ECS-TRV-LOGIN-DEV
```

---

## Instalación

1. Clona el repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tus credenciales de AWS para que boto3 pueda autenticarse.
4. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Estructura del Proyecto

- `main.py` — Entrypoint de la aplicación FastAPI.
- `app/metrics.py` — Lógica para consultar métricas de ECS.
- `app/logs.py` — Lógica para consultar logs de CloudWatch.
- `app/ecs.py` — Lógica para consultar servicios ECS.

## Requisitos

- Python 3.8+
- AWS credentials configuradas (por ejemplo, vía AWS CLI o variables de entorno).

## Notas

- Asegúrate de tener los permisos necesarios en AWS para consultar ECS y CloudWatch Logs.
- Todos los endpoints retornan datos en formato JSON.

---

## Licencia

MIT