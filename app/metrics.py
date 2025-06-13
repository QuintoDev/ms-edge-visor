import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')

def obtener_metricas(cluster_name, service_name):
    metricas = {}
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)

    nombres = ['CpuUtilized', 'MemoryUtilized', 'RunningTaskCount']
    for nombre in nombres:
        response = cloudwatch.get_metric_statistics(
            Namespace='ECS/ContainerInsights',
            MetricName=nombre,
            Dimensions=[
                {'Name': 'ClusterName', 'Value': cluster_name},
                {'Name': 'ServiceName', 'Value': service_name}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Maximum']
        )

        datapoints = response.get('Datapoints', [])
        metricas[nombre] = datapoints[-1]['Maximum'] if datapoints else 0.0

    return metricas
