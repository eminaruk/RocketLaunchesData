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

# Create a dictionary to store success percentages for each company
success_percentages = {}

# Iterate through each launch service and filter launches
for service, country in launch_services.items():
    # Escape special characters in the service name
    service_pattern = re.escape(service)

    # Use str.contains with the escaped pattern
    filtered_launches = launches_df[
        launches_df["launch_service_provider"].str.contains(service_pattern, case=False, na=False)
    ]

    # Exclude companies with zero launches
    if not filtered_launches.empty:
        # Count total launches for the company
        total_launches = len(filtered_launches)

        # Count successful launches for the company
        successful_launches = len(filtered_launches[filtered_launches["status"] == "Launch Successful"])

        # Calculate success percentage, handle division by zero
        success_percentage = (successful_launches / total_launches) * 100 if total_launches > 0 else 0

        # Replace reserved characters in the service name with underscores for both directory and file names
        safe_service_name = service.replace("/", "_").replace(" ", "_")

        # Create a CSV file for each launch service in the output directory
        output_file_path = os.path.join(output_directory, f"{safe_service_name}_launches.csv")
        filtered_launches.to_csv(output_file_path, index=False)

        # Store the success percentage for each company in the dictionary
        success_percentages[service] = success_percentage

# Plotting success percentages for each company
if success_percentages:
    plt.figure(figsize=(12, 6))
    plt.bar(success_percentages.keys(), success_percentages.values(), color='lightgreen')
    plt.xlabel('Company')
    plt.ylabel('Success Percentage')
    plt.title('Success Percentage by Company')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as an image file
    plt.savefig('success_percentage_by_company.png')

    # Show the plot
    plt.show()
else:
    print("No launches found for any company.")
