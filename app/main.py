import logging

from fastapi import FastAPI, Query
from app.metrics import obtener_metricas
from app.logs import obtener_logs
from app.ecs import get_services
from app.utils.logger import get_logger

app = FastAPI()
logger = get_logger('ms-edge-visor.main', level=logging.DEBUG)

@app.get("/metrics")
def leer_metricas(cluster: str, service: str):
    return obtener_metricas(cluster, service)

@app.get("/logs")
def leer_logs(
    logGroup: str,
    minutos: int = Query(5, gt=0, le=60),
    limiteStreams: int = Query(5, gt=1, le=20),
    filtro: str = Query(None, description="Texto para filtrar mensajes")
):
    return obtener_logs(
        log_group=logGroup,
        tiempo_minutos=minutos,
        limite_streams=limiteStreams,
        filtro=filtro
    )

@app.get("/services")
def listar_servicios_ecs(cluster: str):
    logger.debug(f"Cluster received as a parameter {cluster}")
    return get_services(cluster)
