# **AWS Cost Optimization Tool**

This tool helps you optimize costs for AWS services, including **EC2**, **RDS**, **DynamoDB**, and **S3**. It analyzes resource utilization and provides recommendations to reduce costs, such as downsizing underutilized instances, transitioning storage to cheaper classes, and switching DynamoDB tables to on-demand pricing.

## **Features**

- **RDS Optimization**:
  - Identifies underutilized RDS instances based on CPU and storage usage.
  - Recommends downsizing or switching to Reserved Instances.
  - Analyzes RDS snapshots for potential cleanup.
  
- **DynamoDB Optimization**:
  - Reviews read/write capacity utilization.
  - Suggests scaling down or switching to on-demand pricing.
  
- **S3 Optimization**:
  - Detects empty or rarely accessed buckets.
  - Recommends transitioning objects to cheaper storage classes like Glacier.

## **Installation**

Install the required Python libraries:

```bash
pip install boto3 termcolor
```

## **Usage**

Call the `klaudlytics` command:

```python
klaudlytics
```

## **Requirements**
- Python 3.x
- AWS credentials with appropriate permissions (RDS, DynamoDB, S3, CloudWatch, Pricing API)
