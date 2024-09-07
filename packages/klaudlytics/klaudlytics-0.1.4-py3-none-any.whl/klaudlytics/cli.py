import yaml
from klaudlytics.utils.region_utils import prompt_for_regions

def load_config():
    with open('config/services.yaml', 'r') as file:
        return yaml.safe_load(file)

def prompt_user():
    config = load_config()
    services = config['services']

    print("Select the service to optimize cost for or type 'all' for everything:")
    for idx, service in enumerate(services, 1):
        print(f"{idx}. {service['name']} - {service['description']}")
    print("0. Optimize all services")

    choice = input("\nEnter your choice (0 for all): ")
    if choice == '0':
        service_choice = 'all'
    else:
        try:
            service_choice = services[int(choice) - 1]['name']
        except (ValueError, IndexError):
            print("Invalid selection, defaulting to 'all'")
            service_choice = 'all'

    # Prompt for regions after service selection
    selected_regions = prompt_for_regions()
    return service_choice, selected_regions
