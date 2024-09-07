import boto3
from datetime import datetime, timedelta

def get_aws_client(service_name, region):
    return boto3.client(service_name, region_name=region)

def get_ec2_instances(region):
    ec2 = get_aws_client('ec2', region)
    return ec2.describe_instances()

def get_elastic_ips(region):
    ec2 = get_aws_client('ec2', region)
    return ec2.describe_addresses()

def get_ebs_volumes(region):
    ec2 = get_aws_client('ec2', region)
    return ec2.describe_volumes()

def get_snapshots(region):
    ec2 = get_aws_client('ec2', region)
    return ec2.describe_snapshots(OwnerIds=['self'])


def get_image_details(image_id, region):
    """Retrieve details of an AMI by its ImageId."""
    ec2 = get_aws_client('ec2', region)
    response = ec2.describe_images(ImageIds=[image_id])
    
    # Return the first image's details
    if response['Images']:
        return response['Images'][0]
    else:
        print(f"Unable to find image details for AMI {image_id} in {region}.")
        return {}

# RDS Client Functions
def get_rds_instances(region):
    rds = boto3.client('rds', region_name=region)
    return rds.describe_db_instances()

def get_rds_cpu_utilization(db_instance_id, region):
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'DBInstanceIdentifier', 'Value': db_instance_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,  # Hourly metrics
        Statistics=['Average']
    )
    
    datapoints = response.get('Datapoints', [])
    if datapoints:
        total_cpu = sum([datapoint['Average'] for datapoint in datapoints])
        return total_cpu / len(datapoints)
    
    return 0

def get_rds_snapshots(db_instance_id, region):
    rds = boto3.client('rds', region_name=region)
    return rds.describe_db_snapshots(DBInstanceIdentifier=db_instance_id)

# DynamoDB Client Functions
def get_dynamodb_tables(region):
    dynamodb = boto3.client('dynamodb', region_name=region)
    return dynamodb.list_tables()

def get_dynamodb_consumption(table_name, region):
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    
    # Get read capacity utilization
    read_response = cloudwatch.get_metric_statistics(
        Namespace='AWS/DynamoDB',
        MetricName='ConsumedReadCapacityUnits',
        Dimensions=[{'Name': 'TableName', 'Value': table_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )
    
    # Get write capacity utilization
    write_response = cloudwatch.get_metric_statistics(
        Namespace='AWS/DynamoDB',
        MetricName='ConsumedWriteCapacityUnits',
        Dimensions=[{'Name': 'TableName', 'Value': table_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )
    
    # Calculate average utilization
    read_datapoints = read_response.get('Datapoints', [])
    write_datapoints = write_response.get('Datapoints', [])
    
    read_total = sum([datapoint['Sum'] for datapoint in read_datapoints])
    write_total = sum([datapoint['Sum'] for datapoint in write_datapoints])
    
    read_utilization = (read_total / (len(read_datapoints) * 100)) if read_datapoints else 0
    write_utilization = (write_total / (len(write_datapoints) * 100)) if write_datapoints else 0
    
    return {
        'ReadCapacityUnits': read_total,
        'WriteCapacityUnits': write_total,
        'ReadUtilization': read_utilization,
        'WriteUtilization': write_utilization
    }


def get_ebs_volumes(region):
    """Retrieve all EBS volumes in the specified region."""
    ec2 = boto3.client('ec2', region_name=region)
    return ec2.describe_volumes()


def get_ebs_snapshots(region):
    """Retrieve all EBS snapshots in the specified region."""
    ec2 = boto3.client('ec2', region_name=region)
    return ec2.describe_snapshots(OwnerIds=['self'])

def get_volume_iops(volume_id, region):
    """Retrieve CloudWatch IOPS metrics for the specified EBS volume."""
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EBS',
        MetricName='VolumeWriteOps',
        Dimensions=[{'Name': 'VolumeId', 'Value': volume_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,  # Hourly metrics
        Statistics=['Average']
    )
    
    datapoints = response.get('Datapoints', [])
    if datapoints:
        total_iops = sum([datapoint['Average'] for datapoint in datapoints])
        return total_iops / len(datapoints)
    
    return 0

def get_classic_load_balancers(region):
    """Retrieve all Classic Load Balancers in the specified region."""
    elb = boto3.client('elb', region_name=region)
    return elb.describe_load_balancers()

def get_application_load_balancers(region):
    """Retrieve all Application Load Balancers in the specified region."""
    elbv2 = boto3.client('elbv2', region_name=region)
    return elbv2.describe_load_balancers(Names=[])

def get_network_load_balancers(region):
    """Retrieve all Network Load Balancers in the specified region."""
    elbv2 = boto3.client('elbv2', region_name=region)
    return elbv2.describe_load_balancers(Names=[])

def get_target_groups(region):
    """Retrieve all target groups in the specified region."""
    elbv2 = boto3.client('elbv2', region_name=region)
    return elbv2.describe_target_groups()

def get_elb_metrics(elb_name, region, metric_name, elb_type='classic', arn=None):
    """Retrieve CloudWatch metrics for the specified ELB."""
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    if elb_type == 'classic':
        dimensions = [{'Name': 'LoadBalancerName', 'Value': elb_name}]
    else:
        dimensions = [{'Name': 'LoadBalancer', 'Value': arn}]
    
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ELB' if elb_type == 'classic' else 'AWS/ApplicationELB',
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # Daily stats
        Statistics=['Sum']
    )
    
    datapoints = response.get('Datapoints', [])
    if datapoints:
        total_requests = sum([datapoint['Sum'] for datapoint in datapoints])
        return total_requests
    
    return 0


def get_s3_buckets(region):
    """Retrieve all S3 buckets in the specified region."""
    s3 = boto3.client('s3', region_name=region)
    return s3.list_buckets()

def get_s3_bucket_metrics(bucket_name, region, metric):
    """Retrieve metrics (e.g., object count, size) for the specified S3 bucket."""
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)  # Analyze the last 30 days
    
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/S3',
        MetricName=metric,
        Dimensions=[{'Name': 'BucketName', 'Value': bucket_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # Daily metrics
        Statistics=['Sum']
    )
    
    datapoints = response.get('Datapoints', [])
    if datapoints:
        total = sum([datapoint['Sum'] for datapoint in datapoints])
        return total
    
    return 0

def get_s3_objects(bucket_name, region):
    """Retrieve all objects from the specified S3 bucket."""
    s3 = boto3.client('s3', region_name=region)
    paginator = s3.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(Bucket=bucket_name)
    
    objects = []
    for page in response_iterator:
        objects.extend(page.get('Contents', []))
    
    return objects
