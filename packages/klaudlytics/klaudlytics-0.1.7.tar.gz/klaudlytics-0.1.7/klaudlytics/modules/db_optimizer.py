from utils.aws_client import get_rds_instances, get_rds_cpu_utilization, get_rds_snapshots, get_dynamodb_tables, get_dynamodb_consumption
from datetime import datetime, timedelta, timezone
from termcolor import colored
import boto3

def optimize(regions):
    print(f"Optimizing DB costs for regions: {regions}")
    
    for region in regions:
        print(f"\n--- Scanning region {region} ---")
        optimize_dynamodb_tables(region)
        optimize_rds_instances(region)

# Optimizing RDS Instances
def optimize_rds_instances(region):
    print(f"\n[RDS Instances] Optimizing RDS instances in {region}")
    try:
        rds_instances = get_rds_instances(region)
        if len(rds_instances['DBInstances']) == 0:
            print(colored(f"No RDS instances found in {region}",'red'))
    except Exception as e:
        print(f"Error retrieving RDS instances in {region}: {e}")
        return

    for db_instance in rds_instances['DBInstances']:
        db_id = db_instance['DBInstanceIdentifier']
        db_class = db_instance['DBInstanceClass']
        db_status = db_instance['DBInstanceStatus']
        db_storage = db_instance['AllocatedStorage']
        db_engine = db_instance['Engine']
        db_multiaz = db_instance['MultiAZ']

        if db_status == 'available':
            # CPU utilization check
            db_cpu_usage = get_rds_cpu_utilization(db_id, region)
            if db_cpu_usage < 10:
                print_rds_recommendation(db_id, "underutilized", db_cpu_usage)
            
            # Storage optimization
            if db_storage > 100:
                print_rds_recommendation(db_id, "large_storage", db_storage)
            
            # Reserved Instance recommendation
            recommend_rds_reserved_instance(db_id, db_class, region, db_engine, db_multiaz)

        # Optimize RDS snapshots
        optimize_rds_snapshots(db_id, region)

# RDS Reserved Instance Recommendation
def recommend_rds_reserved_instance(db_id, db_class, region, db_engine, db_multiaz):
    pricing = boto3.client('pricing', region_name='us-east-1')
    
    # Mapping AWS region codes to human-readable locations for Pricing API
    region_map = {
        'us-east-1': 'US East (N. Virginia)',
        'us-west-1': 'US West (N. California)',
        # Add other region mappings as necessary
    }
    pricing_region = region_map.get(region, region)

    try:
        response = pricing.get_products(
            ServiceCode='AmazonRDS',
            Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': db_class},
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': pricing_region},
                {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': db_engine},
                {'Type': 'TERM_MATCH', 'Field': 'deploymentOption', 'Value': 'Multi-AZ' if db_multiaz else 'Single-AZ'}
            ]
        )
        
        pricing_data = response.get('PriceList', [])
        if pricing_data:
            print(f"Consider switching RDS Instance {db_id} to Reserved Instances for cost savings.")
        else:
            print(f"Could not retrieve pricing data for RDS Instance {db_id} in {region}.")
    except Exception as e:
        print(f"Error retrieving pricing data for RDS Instance {db_id} in {region}: {e}")

# Optimizing RDS Snapshots
def optimize_rds_snapshots(db_id, region):
    """Check and recommend actions for RDS snapshots."""
    try:
        snapshots = get_rds_snapshots(db_id, region)
    except Exception as e:
        print(f"Error retrieving RDS snapshots for {db_id} in {region}: {e}")
        return
    
    for snapshot in snapshots['DBSnapshots']:
        snapshot_id = snapshot['DBSnapshotIdentifier']
        snapshot_date = snapshot['SnapshotCreateTime']
        
        if is_snapshot_old(snapshot_date):
            print(f"RDS Snapshot {snapshot_id} for {db_id} is older than 90 days. Consider deleting it to save storage costs.")

# Optimizing DynamoDB Tables
def optimize_dynamodb_tables(region):
    print(f"\n[DynamoDB] Optimizing DynamoDB tables in {region}")
    try:
        dynamodb_tables = get_dynamodb_tables(region)
        if len(dynamodb_tables['TableNames']) == 0:
            print(colored(f"No DynamoDB tables found in {region}.",'red'))
    except Exception as e:
        print(f"Error retrieving DynamoDB tables in {region}: {e}")
        return
    
    for table in dynamodb_tables['TableNames']:
        table_name = table
        
        # Get read/write capacity utilization
        try:
            consumption = get_dynamodb_consumption(table_name, region)
        except Exception as e:
            print(f"Error retrieving consumption data for DynamoDB table {table_name} in {region}: {e}")
            continue
        
        read_capacity = consumption['ReadCapacityUnits']
        write_capacity = consumption['WriteCapacityUnits']
        read_utilization = consumption['ReadUtilization']
        write_utilization = consumption['WriteUtilization']
        
        # Recommend scaling down if utilization is low
        if read_utilization < 10:
            print_dynamodb_recommendation(table_name, "read", read_utilization)
        
        if write_utilization < 10:
            print_dynamodb_recommendation(table_name, "write", write_utilization)
        
        # Check if the table can be switched to on-demand pricing
        if should_switch_to_on_demand(read_utilization, write_utilization):
            print(f"DynamoDB Table {table_name} has low utilization. Consider switching to on-demand pricing for cost savings.")

def should_switch_to_on_demand(read_utilization, write_utilization):
    """Determine if a DynamoDB table should switch to on-demand pricing."""
    # If both read and write utilization are consistently below 10%, switch to on-demand pricing
    return read_utilization < 10 and write_utilization < 10

# Helper Functions
def is_snapshot_old(snapshot_date):
    """Determine if the snapshot is older than 90 days."""
    now = datetime.now(timezone.utc)
    return snapshot_date < (now - timedelta(days=90))

# Pretty Print Recommendations
def print_rds_recommendation(db_id, recommendation_type, value):
    if recommendation_type == "underutilized":
        print(f"\nRDS Instance {db_id}:")
        print(colored(f"  - CPU Usage: {value}% (Underutilized)", "yellow"))
        print(colored(f"  - Recommendation: Consider downsizing the instance class.", "green"))
    elif recommendation_type == "large_storage":
        print(f"\nRDS Instance {db_id}:")
        print(colored(f"  - Storage: {value} GB", "yellow"))
        print(colored(f"  - Recommendation: Consider moving to cheaper storage if rarely accessed.", "green"))

def print_dynamodb_recommendation(table_name, capacity_type, utilization):
    print(f"\nDynamoDB Table {table_name}:")
    if capacity_type == "read":
        print(colored(f"  - Read Capacity Utilization: {utilization}%", "yellow"))
        print(colored("  - Recommendation: Consider scaling down read capacity.", "green"))
    elif capacity_type == "write":
        print(colored(f"  - Write Capacity Utilization: {utilization}%", "yellow"))
        print(colored("  - Recommendation: Consider scaling down write capacity.", "green"))
