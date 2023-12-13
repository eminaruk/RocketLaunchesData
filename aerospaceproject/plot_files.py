import os
import matplotlib.pyplot as plt
import csv

# Specify the directory where country-specific CSV files are stored
output_directory = 'country_csv_files'

# Plotting the launch data
launch_counts = {}
success_percentages = {}

# Iterate through each file in the directory
for filename in os.listdir(output_directory):
    if filename.endswith(".csv"):
        country = os.path.splitext(filename)[0]  # Extract country name from the filename
        with open(os.path.join(output_directory, filename), 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip the header row
            total_launches = 0
            failure_launches = 0
            successful_launches = 0
            for row in csv_reader:
                
                if row[-1] == 'Launch Successful':  # Assuming the launch outcome is in the last column
                    successful_launches += 1
                if row[-1] == 'Launch Failure':
                    failure_launches +=1

            total_launches = successful_launches + failure_launches
            # Calculate success percentage
            success_percentage = (successful_launches / total_launches) * 100 if total_launches > 0 else 0
            
            # Store the results
            launch_counts[country] = total_launches
            success_percentages[country] = success_percentage

# Filter out countries with zero launches
launch_counts = {country: launches for country, launches in launch_counts.items() if launches > 0}
success_percentages = {country: percentage for country, percentage in success_percentages.items() if country in launch_counts}

# Create a bar chart for the number of launches
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.bar(launch_counts.keys(), launch_counts.values(), color='skyblue')
plt.xlabel('Country')
plt.ylabel('Number of Launches')
plt.title('Number of Launches by Country')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Create a bar chart for success percentages
plt.subplot(1, 2, 2)
plt.bar(success_percentages.keys(), success_percentages.values(), color='lightgreen')
plt.xlabel('Country')
plt.ylabel('Success Percentage')
plt.title('Success Percentage by Country')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save or display the plots
plt.savefig('launches_and_success_percentages_by_country.png')
plt.show()
