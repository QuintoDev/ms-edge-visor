import boto3
import json

ecs = boto3.client('ecs')

def get_services(cluster: str):
    services_status = {}
    next_token = None

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

    return services_status
