import csv
import json
import os

# Load the JSON data
with open('services_by_country.json', 'r', encoding='utf-8') as json_file:
    services_by_country = json.load(json_file)

# Load the CSV data
with open('launches.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Create a directory to store country-specific CSV files
    output_directory = 'country_csv_files'
    os.makedirs(output_directory, exist_ok=True)

    # Create CSV files for each country
    country_files = {}
    for country in services_by_country:
        country_filename = os.path.join(output_directory, f'{country}.csv')
        country_files[country] = open(country_filename, 'a', newline='', encoding='utf-8')
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(country_files[country], fieldnames=fieldnames)
        csv_writer.writeheader()

    # Iterate through the CSV rows
    for row in csv_reader:
        # Get the launch service provider
        launch_service_provider = row['launch_service_provider']

        # Find the country of the launch service provider
        country = 'Unknown'  # Default to 'Unknown' if the country is not found
        for c, providers in services_by_country.items():
            if launch_service_provider in providers:
                country = c
                break

        # Check if the country is known
        if country != 'Unknown':
            # Write the row to the corresponding CSV file
            csv_writer = csv.DictWriter(country_files[country], fieldnames=fieldnames)
            csv_writer.writerow(row)

# Close all country-specific CSV files
for country_file in country_files.values():
    country_file.close()

print(f"Filtering completed. Check the '{output_directory}' directory for country-specific CSV files.")
