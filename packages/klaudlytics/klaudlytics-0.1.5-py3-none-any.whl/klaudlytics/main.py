from cli import prompt_user
from klaudlytics.modules import ec2_optimizer, s3_optimizer, db_optimizer

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
    service_choice, selected_regions = prompt_user()

    if service_choice == 'all':
        for service in ['ec2', 's3', 'db']:
            run_optimizer(service, selected_regions)
    else:
        run_optimizer(service_choice, selected_regions)

if __name__ == "__main__":
    main()
