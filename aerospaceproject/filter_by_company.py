import os
import pandas as pd
import re

# Read launch services from service_providers.txt
with open("service_providers.txt", "r") as file:
    launch_services = dict(line.strip().split(": ", 1) for line in file)

# Read launches from launches.csv
launches_df = pd.read_csv("launches.csv")

# Create the output directory if it doesn't exist
output_directory = "company_csv_files"
os.makedirs(output_directory, exist_ok=True)

# Iterate through each launch service and filter launches
for service, country in launch_services.items():
    # Escape special characters in the service name
    service_pattern = re.escape(service)
    
    # Use str.contains with the escaped pattern
    filtered_launches = launches_df[launches_df["launch_service_provider"].str.contains(service_pattern, case=False, na=False)]

    # Replace reserved characters in the service name with underscores for both directory and file names
    safe_service_name = service.replace("/", "_").replace(" ", "_")
    
    # Create a CSV file for each launch service in the output directory
    output_file_path = os.path.join(output_directory, f"{safe_service_name}_launches.csv")
    filtered_launches.to_csv(output_file_path, index=False)

print("CSV files saved in the 'company_csv_files' directory.")
