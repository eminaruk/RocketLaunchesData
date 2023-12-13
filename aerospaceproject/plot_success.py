import os
import matplotlib.pyplot as plt
import csv

# Specify the directory where country-specific CSV files are stored
output_directory = 'country_csv_files'

# Iterate through each file in the directory
for filename in os.listdir(output_directory):
    if filename.endswith(".csv"):
        country = os.path.splitext(filename)[0]  # Extract country name from the filename

        with open(os.path.join(output_directory, filename), 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Count success and failure
            success_count = 0
            failure_count = 0

            for row in csv_reader:
                if row['status'] == 'Launch Successful':
                    success_count += 1
                else:
                    failure_count += 1

            # Plot the data only if there are launches
            if success_count + failure_count > 0:
                # Plot the data with different colors
                labels = ['Success', 'Failure']
                values = [success_count, failure_count]
                colors = ['lightgreen', 'lightcoral']  # You can customize colors here

                plt.bar(labels, values, color=colors)
                plt.xlabel('Mission Status')
                plt.ylabel('Number of Launches')
                plt.title(f'Launches in {country} by Mission Status')
                plt.show()
