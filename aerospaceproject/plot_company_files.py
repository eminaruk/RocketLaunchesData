import os
import pandas as pd
import re
import matplotlib.pyplot as plt

# Read launch services from service_providers.txt
with open("service_providers.txt", "r") as file:
    launch_services = dict(line.strip().split(": ", 1) for line in file)

# Read launches from launches.csv
launches_df = pd.read_csv("launches.csv")

# Create the output directory if it doesn't exist
output_directory = "company_csv_files"
os.makedirs(output_directory, exist_ok=True)

# Create a dictionary to store the launch counts for each company
launch_counts = {}

# Iterate through each launch service and filter launches
for service, country in launch_services.items():
    # Escape special characters in the service name
    service_pattern = re.escape(service)

    # Use str.contains with the escaped pattern
    filtered_launches = launches_df[
        (launches_df["launch_service_provider"].str.contains(service_pattern, case=False, na=False)) &
        (launches_df["status"] == "Launch Successful")
    ]

    # Replace reserved characters in the service name with underscores for both directory and file names
    safe_service_name = service.replace("/", "_").replace(" ", "_")

    # Create a CSV file for each launch service in the output directory
    output_file_path = os.path.join(output_directory, f"{safe_service_name}_launches.csv")
    filtered_launches.to_csv(output_file_path, index=False)

    # Only count launches for companies that have at least one successful launch
    if len(filtered_launches) > 0:
        # Store the launch count for each company in the dictionary
        launch_counts[service] = len(filtered_launches)

# Plotting
if launch_counts:
    plt.figure(figsize=(12, 6))
    plt.bar(launch_counts.keys(), launch_counts.values(), color='skyblue')
    plt.xlabel('Company')
    plt.ylabel('Number of Successful Launches')
    plt.title('Number of Successful Launches by Company')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as an image file
    plt.savefig('successful_launch_counts_by_company.png')

    # Show the plot
    plt.show()
else:
    print("No successful launches found for any company.")
