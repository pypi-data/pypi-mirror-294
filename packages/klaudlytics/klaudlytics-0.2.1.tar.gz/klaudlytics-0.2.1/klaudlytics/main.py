from klaudlytics.cli import prompt_user, load_config
from klaudlytics.modules import ec2_optimizer, s3_optimizer, db_optimizer
import argparse

def run_optimizer(service_name, regions):
    if service_name == 'ec2':
        ec2_optimizer.optimize(regions)
    elif service_name == 's3':
        s3_optimizer.optimize(regions)
    elif service_name == 'db':
        db_optimizer.optimize(regions)
    else:
        print(f"Unknown service: {service_name}")


def main():
    parser = argparse.ArgumentParser(description="Klaudlytics Cloud Cost Optimization Tool")
    
    # Add an argument to receive the config file path
    parser.add_argument(
        '--config', 
        type=str, 
        required=True, 
        help="Path to the services.yaml file"
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Load the config file using the provided file path
    config = load_config(args.config)
    service_choice, selected_regions = prompt_user(config)

    if service_choice == 'all':
        for service in ['ec2', 's3', 'db']:
            run_optimizer(service, selected_regions)
    else:
        run_optimizer(service_choice, selected_regions)

if __name__ == "__main__":
    main()
