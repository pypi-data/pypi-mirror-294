from klaudlytics.utils.aws_client import get_s3_buckets, get_s3_bucket_metrics, get_s3_objects
from termcolor import colored
from datetime import datetime, timedelta

def optimize(regions):
    print(f"Optimizing S3 costs for regions: {regions}")
    
    for region in regions:
        print(f"\n--- Scanning region {region} ---")
        optimize_s3_buckets(region)

def optimize_s3_buckets(region):
    """Optimize S3 buckets in the specified region."""
    print(f"\n[S3 Buckets] Checking for cost-saving opportunities in {region}")
    try:
        buckets = get_s3_buckets(region)
    except Exception as e:
        print(f"Error retrieving S3 buckets in {region}: {e}")
        return

    for bucket in buckets.get('Buckets', []):
        bucket_name = bucket['Name']
        
        # Check if the bucket is empty
        try:
            object_count = get_s3_bucket_metrics(bucket_name, region, metric='NumberOfObjects')
            if object_count == 0:
                print_pretty_s3_output(bucket_name, status="empty")
                continue  # Skip further checks for empty buckets
        except Exception as e:
            print(f"Error retrieving metrics for S3 bucket {bucket_name}: {e}")
            continue
        
        # Check if the bucket has been accessed recently
        try:
            access_count = get_s3_bucket_metrics(bucket_name, region, metric='BucketSizeBytes')
            if access_count == 0:
                print_pretty_s3_output(bucket_name, status="no_access")
        except Exception as e:
            print(f"Error retrieving access data for S3 bucket {bucket_name}: {e}")
        
        # Optimize individual objects in the bucket
        optimize_s3_objects(bucket_name, region)

def optimize_s3_objects(bucket_name, region):
    """Optimize objects stored in S3 buckets by transitioning to cheaper storage classes."""
    try:
        s3_objects = get_s3_objects(bucket_name, region)
    except Exception as e:
        print(f"Error retrieving objects in S3 bucket {bucket_name}: {e}")
        return
    
    for obj in s3_objects:
        object_key = obj['Key']
        storage_class = obj['StorageClass']
        last_accessed = obj.get('LastAccessedTime')  # Optional: Requires S3 analytics setup
        
        # Recommend transitioning to Infrequent Access or Glacier for older objects
        if storage_class == 'STANDARD' and is_old_object(last_accessed):
            print_pretty_s3_object_output(bucket_name, object_key, "transition_to_ia_or_glacier")
        
        # Recommend enabling lifecycle policies for the bucket
        recommend_lifecycle_policy(bucket_name)

def recommend_lifecycle_policy(bucket_name):
    """Recommend enabling lifecycle policies for buckets to automatically transition objects."""
    print(f"Bucket {bucket_name} does not have a lifecycle policy. Recommend adding one to automatically transition objects to cheaper storage classes after a defined period.")

def is_old_object(last_accessed):
    """Determine if an object hasn't been accessed in over 30 days."""
    if last_accessed:
        return last_accessed < (datetime.now() - timedelta(days=30))
    return False  # Default to False if we can't determine access time

# Pretty print for S3 optimization output
def print_pretty_s3_output(bucket_name, status):
    if status == "empty":
        print(f"\nS3 Bucket {bucket_name}:")
        print(colored("  - Status: Empty.", "yellow"))
        print(colored("  - Recommendation: Consider deleting to save storage costs.", "green"))
    elif status == "no_access":
        print(f"\nS3 Bucket {bucket_name}:")
        print(colored("  - Status: No recent access.", "yellow"))
        print(colored("  - Recommendation: Consider transitioning objects to Glacier or deleting the bucket if no longer needed.", "green"))

def print_pretty_s3_object_output(bucket_name, object_key, action):
    if action == "transition_to_ia_or_glacier":
        print(f"\nObject {object_key} in S3 Bucket {bucket_name}:")
        print(colored("  - Status: Hasn't been accessed recently.", "yellow"))
        print(colored("  - Recommendation: Consider transitioning to Infrequent Access or Glacier.", "green"))
