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

# Create a directory for PNG files
png_directory = "ind_company_png_files"
os.makedirs(png_directory, exist_ok=True)

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
        # Filter only successful and failed launches
        filtered_launches = filtered_launches[filtered_launches["status"].isin(["Launch Successful", "Launch Failure"])]

        # Replace reserved characters in the service name with underscores for both directory and file names
        safe_service_name = service.replace("/", "_").replace(" ", "_")

        # Create a CSV file for each launch service in the output directory
        output_file_path = os.path.join(output_directory, f"{safe_service_name}_launches.csv")
        filtered_launches.to_csv(output_file_path, index=False)

        # Count successful and failed launches for the company
        success_counts = filtered_launches["status"].value_counts()

        # Check if the DataFrame is not empty before plotting
        if not success_counts.empty:
            # Plotting successful and failed launches for each company
            plt.figure(figsize=(8, 6))
            success_counts.plot(kind='bar', color=['green', 'red'])
            plt.title(f'Success and Failure Quantities for {service}')
            plt.xlabel('Outcome')
            plt.ylabel('Quantity')
            plt.xticks(rotation=0)
            plt.tight_layout()

            # Save the plot as an image file in the PNG directory
            png_file_path = os.path.join(png_directory, f'success_failure_quantities_{safe_service_name}.png')
            plt.savefig(png_file_path)

            # Show the plot
            plt.close()
        else:
            print(f"No successful or failed launches found for {service}.")
    else:
        print(f"No launches found for {service}.")

print("PNG files saved in the 'ind_company_png_files' directory.")
