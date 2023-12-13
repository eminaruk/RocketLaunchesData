import json

# Read data from the file
with open('service_providers.txt', 'r') as file:
    data = file.readlines()

# Create a dictionary to store services by country
services_by_country = {}

# Process each line of data
for line in data:
    line = line.strip()
    if line:

        service, country = line.split(': ')

        if country not in services_by_country:
            services_by_country[country] = [service]
        else:
            services_by_country[country].append(service)

# Print services grouped by country
for country, services in services_by_country.items():
    print(f"{country}: {', '.join(services)}")

# Save services_by_country as a JSON file
with open('services_by_country.json', 'w') as json_file:
    json.dump(services_by_country, json_file, indent=2)

print("JSON file saved as 'services_by_country.json'")
