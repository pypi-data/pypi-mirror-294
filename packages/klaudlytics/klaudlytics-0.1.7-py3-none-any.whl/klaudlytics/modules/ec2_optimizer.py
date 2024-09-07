from utils.aws_client import get_ec2_instances, get_elastic_ips, get_ebs_volumes, get_snapshots, get_image_details, get_ebs_snapshots, get_volume_iops
from utils.aws_client import get_classic_load_balancers, get_application_load_balancers, get_network_load_balancers, get_target_groups, get_elb_metrics
from termcolor import colored
import boto3
from datetime import datetime, timedelta, timezone

# Main optimization function
def optimize(regions):
    print(f"Optimizing costs for regions: {regions}")
    
    for region in regions:
        print(f"\n--- Scanning region {region} ---")
        
        # Optimize EC2 Instances
        optimize_ec2_instances(region)
        
        # Optimize Elastic IPs
        optimize_elastic_ips(region)
        
        # Optimize EBS Volumes
        optimize_ebs_volumes(region)
        
        # Optimize Snapshots
        optimize_snapshots(region)
        optimize_ebs_snapshots(region)
        
        # Optimize Load Balancers
        optimize_classic_load_balancers(region)
        optimize_application_load_balancers(region)
        optimize_network_load_balancers(region)
        optimize_target_groups(region)

# Pretty Print Functions
def print_ec2_optimization(instance_id, cpu_utilization, is_underutilized, pricing_data, is_reserved_recommendation):
    print(f"\nInstance {instance_id}:")
    if cpu_utilization is not None:
        print(f"  - Average CPU utilization: {cpu_utilization:.2f}%")
    if is_underutilized:
        print(colored("  - Recommendation: Consider resizing to a smaller instance type (underutilized).", "yellow"))
    if is_reserved_recommendation:
        print(colored("  - Recommendation: Running more than 75% of the time. Suggest Reserved Instance or Savings Plan.", "green"))
    if pricing_data:
        print(f"  - Pricing Data: {pricing_data}")
    else:
        print(colored("  - Pricing Data: Not available.", "red"))

def print_elastic_ip_optimization(elastic_ip, is_unused):
    print(f"\nElastic IP {elastic_ip}:")
    if is_unused:
        print(colored("  - Status: Not associated with any instance.", "yellow"))
        print(colored("  - Recommendation: Consider releasing it to avoid unnecessary charges.", "green"))

def print_ebs_optimization(volume_id, volume_size, is_unattached, is_provisioned_iops, is_underutilized):
    print(f"\nEBS Volume {volume_id}:")
    if is_unattached:
        print(colored("  - Status: Unattached.", "yellow"))
        print(colored("  - Recommendation: Consider deleting it to avoid unnecessary storage costs.", "green"))
    if volume_size > 100:
        print(f"  - Size: {volume_size} GiB")
        print(colored("  - Recommendation: Ensure it's actively in use to avoid high storage costs.", "green"))
    if is_provisioned_iops and is_underutilized:
        print(colored("  - Recommendation: Underutilized provisioned IOPS. Consider downgrading to gp3 for cost savings.", "yellow"))

def print_elb_optimization(elb_name, request_count, is_idle, load_balancer_type):
    print(f"\n{load_balancer_type} Load Balancer {elb_name}:")
    if is_idle:
        print(colored(f"  - Status: Idle, with {request_count} requests.", "yellow"))
        print(colored(f"  - Recommendation: Consider deleting or switching to a more cost-effective solution.", "green"))

# EC2 Optimization
def optimize_ec2_instances(region):
    print(f"\n[EC2 Instances] Optimizing EC2 instances in {region}")
    instances = get_ec2_instances(region)

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']

            # Determine OS type
            image_id = instance['ImageId']
            os_type = determine_os_type(image_id, region)

            # Get CPU utilization
            cpu_utilization = get_instance_cpu_utilization(instance_id, region)
            is_underutilized = cpu_utilization < 10 if cpu_utilization is not None else False

            # Reserved Instance recommendation
            is_reserved_recommendation = check_reserved_instance_recommendation(instance_id, instance_type, region)

            # Pricing data
            pricing_data = get_pricing_data(instance_type, region, os_type)

            # Use the pretty print function
            print_ec2_optimization(
                instance_id, 
                cpu_utilization, 
                is_underutilized, 
                pricing_data, 
                is_reserved_recommendation
            )

def determine_os_type(image_id, region):
    image_details = get_image_details(image_id, region)
    image_name = image_details.get('Name', '').lower()

    if 'windows' in image_name:
        return 'Windows'
    elif 'amzn' in image_name or 'ubuntu' in image_name or 'linux' in image_name:
        return 'Linux'
    else:
        return 'Unknown'

# Elastic IP Optimization
def optimize_elastic_ips(region):
    print(f"\n[Elastic IPs] Checking for unused Elastic IPs in {region}")
    elastic_ips = get_elastic_ips(region)

    for eip in elastic_ips['Addresses']:
        public_ip = eip['PublicIp']
        is_unused = 'InstanceId' not in eip

        # Use the pretty print function
        print_elastic_ip_optimization(public_ip, is_unused)

# EBS Volume Optimization
def optimize_ebs_volumes(region):
    print(f"\n[EBS Volumes] Checking for cost-saving opportunities in {region}")
    volumes = get_ebs_volumes(region)

    for volume in volumes['Volumes']:
        volume_id = volume['VolumeId']
        volume_size = volume['Size']  # in GiB
        is_unattached = volume['State'] == 'available'
        is_provisioned_iops = volume['VolumeType'] in ['io1', 'io2']
        iops = volume.get('Iops', 0)
        actual_iops = get_volume_iops(volume_id, region) if is_provisioned_iops else 0
        is_underutilized = is_provisioned_iops and actual_iops < 0.1 * iops

        # Use the pretty print function
        print_ebs_optimization(volume_id, volume_size, is_unattached, is_provisioned_iops, is_underutilized)

    # Optimize EBS snapshots
    optimize_ebs_snapshots(region)

# EBS Snapshot Optimization
def optimize_ebs_snapshots(region):
    snapshots = get_ebs_snapshots(region)

    for snapshot in snapshots['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        snapshot_date = snapshot['StartTime']
        
        if is_snapshot_old(snapshot_date):
            print(f"EBS Snapshot {snapshot_id} is older than 90 days. Consider deleting it to save storage costs.")

# Snapshot Optimization
def optimize_snapshots(region):
    print(f"\n[Snapshots] Checking for redundant snapshots in {region}")
    snapshots = get_snapshots(region)

    for snapshot in snapshots['Snapshots']:
        if snapshot['State'] == 'completed':
            if is_snapshot_old(snapshot['StartTime']):
                print(f"Snapshot {snapshot['SnapshotId']} is older than 90 days. Consider deleting to save storage costs.")

# Load Balancer Optimization
def optimize_classic_load_balancers(region):
    print(f"\n[Classic Load Balancers] Optimizing Classic Load Balancers in {region}")
    classic_elbs = get_classic_load_balancers(region)

    for elb in classic_elbs['LoadBalancerDescriptions']:
        elb_name = elb['LoadBalancerName']
        request_count = get_elb_metrics(elb_name, region, metric_name='RequestCount', elb_type='classic')
        is_idle = request_count < 100

        # Use the pretty print function
        print_elb_optimization(elb_name, request_count, is_idle, "Classic")

def optimize_application_load_balancers(region):
    alb_elbs = get_application_load_balancers(region)

    for alb in alb_elbs['LoadBalancers']:
        alb_name = alb['LoadBalancerName']
        alb_arn = alb['LoadBalancerArn']
        request_count = get_elb_metrics(alb_name, region, metric_name='RequestCount', elb_type='application', arn=alb_arn)
        is_idle = request_count < 100

        # Use the pretty print function
        print_elb_optimization(alb_name, request_count, is_idle, "Application")

def optimize_network_load_balancers(region):
    nlb_elbs = get_network_load_balancers(region)

    for nlb in nlb_elbs['LoadBalancers']:
        nlb_name = nlb['LoadBalancerName']
        nlb_arn = nlb['LoadBalancerArn']
        request_count = get_elb_metrics(nlb_name, region, metric_name='ActiveFlowCount', elb_type='network', arn=nlb_arn)
        is_idle = request_count < 100

        # Use the pretty print function
        print_elb_optimization(nlb_name, request_count, is_idle, "Network")

def optimize_target_groups(region):
    try:
        target_groups = get_target_groups(region)
    except Exception as e:
        print(f"Error retrieving target groups in region {region}: {e}")
        return

    for target_group in target_groups.get('TargetGroups', []):
        tg_name = target_group['TargetGroupName']
        targets = target_group.get('Targets', [])
        target_count = len(targets)

        if target_count == 0:
            print_target_group_optimization(tg_name)

def print_target_group_optimization(tg_name):
    """Pretty print for target group optimization recommendations."""
    print(f"\nTarget Group {tg_name}:")
    print(colored("  - Status: No registered targets.", "yellow"))
    print(colored("  - Recommendation: Consider deleting it to reduce unnecessary resources.", "green"))

# Helper Functions
def get_instance_cpu_utilization(instance_id, region):
    cloudwatch = boto3.client('cloudwatch', region_name=region)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )

    datapoints = response.get('Datapoints', [])
    if not datapoints:
        print(f"No CPU utilization data available for instance {instance_id}")
        return 0

    total_cpu_utilization = sum([point['Average'] for point in datapoints])
    average_cpu_utilization = total_cpu_utilization / len(datapoints)

    print(f"Instance {instance_id} average CPU utilization over the past week: {average_cpu_utilization:.2f}%")
    return average_cpu_utilization

def check_reserved_instance_recommendation(instance_id, instance_type, region):
    cloudwatch = boto3.client('cloudwatch', region_name=region)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=30)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=['SampleCount']
    )

    active_days = sum([datapoint['SampleCount'] > 0 for datapoint in response.get('Datapoints', [])])

    return active_days > (0.75 * 30)

def get_pricing_data(instance_type, region, os_type):
    pricing = boto3.client('pricing', region_name='us-east-1')
    response = pricing.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': os_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region}
        ]
    )

    pricing_data = response.get('PriceList', [])
    return pricing_data if pricing_data else None

def is_snapshot_old(snapshot_date):
    now = datetime.now(timezone.utc)
    return snapshot_date < (now - timedelta(days=90))
