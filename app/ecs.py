import boto3
import logging

from botocore.exceptions import ClientError
from app.utils.logger import get_logger
from fastapi import HTTPException

ecs = boto3.client('ecs')
logger = get_logger('ms-edge-visor.ecs', level=logging.DEBUG)

def get_services(cluster: str):
    services_status = {}
    next_token = None

    try:
        while True:
            if next_token:
                response = ecs.list_services(cluster=cluster, nextToken=next_token)
            else:
                response = ecs.list_services(cluster=cluster)

            service_arns = response['serviceArns']
            if not service_arns:
                break

            for i in range(0, len(service_arns), 10):
                batch = service_arns[i:i+10]
                details = ecs.describe_services(cluster=cluster, services=batch)
                for service in details['services']:
                    services_status[service['serviceName']] = {
                        'running': service['runningCount'],
                        'desired': service['desiredCount']
                    }

            next_token = response.get('nextToken')
            if not next_token:
                break

        logger.info(f"Data obtained for {len(service_arns)} ecs services")
        logger.debug("Returning response")
        return services_status
    
    except ClientError as e:
        logger.error(f"{e.response['Error']['Message']}")
        raise HTTPException(status_code=404, detail="No services found.")
