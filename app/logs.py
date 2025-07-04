import boto3
import logging

from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone
from app.utils.logger import get_logger
from fastapi import HTTPException

logger = get_logger('ms-edge-visor.logs', level=logging.DEBUG)
logs = boto3.client('logs')
COLOMBIA_TZ = timezone(timedelta(hours=-5))

def obtener_logs(log_group, tiempo_minutos=5, limite_streams=5, filtro: str = None):
    end_time = int(datetime.now(COLOMBIA_TZ).timestamp() * 1000)
    start_time = end_time - tiempo_minutos * 60 * 1000
    all_logs = []

    try:
        response_streams = logs.describe_log_streams(
            logGroupName=log_group,
            orderBy='LastEventTime',
            descending=True,
            limit=limite_streams
        )

        log_streams = [s['logStreamName'] for s in response_streams.get('logStreams', [])]
        

        filtro = filtro.strip().lower() if filtro else None

        for stream in log_streams:
            eventos = logs.get_log_events(
                logGroupName=log_group,
                logStreamName=stream,
                startTime=start_time,
                endTime=end_time,
                limit=100,
                startFromHead=False
            )

            for e in eventos.get('events', []):
                mensaje = e['message']
                normalizado = mensaje.lower()

                if filtro is None or filtro in normalizado:
                    all_logs.append({
                        "stream": stream,
                        "message": mensaje
                    })
            
        return {
            "logGroup": log_group,
            "tiempoMinutos": tiempo_minutos,
            "filtro": filtro,
            "totalEventos": len(all_logs),
            "logs": all_logs
        }
    
    except ClientError as e:
        logger.error(f"{e.response['Error']['Message']}")
        raise HTTPException(status_code=404, detail="No logs found.")
