def get_available_regions():
    return ['us-east-1', 'us-west-1', 'eu-west-1', 'ap-southeast-1']

def prompt_for_regions():
    regions = get_available_regions()
    print("Select regions to scan (comma separated for multiple regions) or type 'all':")
    for idx, region in enumerate(regions, 1):
        print(f"{idx}. {region}")
    print("0. All regions")

    selected = input("\nEnter your choice (e.g. 1,2 for multiple regions or 0 for all): ")
    if selected == '0':
        return regions
    else:
        try:
            indices = list(map(int, selected.split(',')))
            return [regions[i - 1] for i in indices]
        except (ValueError, IndexError):
            print("Invalid input. Defaulting to all regions.")
            return regions
