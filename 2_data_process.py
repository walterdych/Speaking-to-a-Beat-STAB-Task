import os
import glob
import csv
import re

def process_log_to_csv(log_file_path, csv_file_path):
    with open(log_file_path, 'r') as log_file, open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Writing the header of the CSV file
        csv_writer.writerow(['Timestamp', 'Log Level', 'Message'])
        
        for line in log_file:
            # Extracting the timestamp, log level, and message using regular expressions
            match = re.match(r'([0-9.]+) \t([A-Z]+) \t(.+)', line)
            if match:
                timestamp, log_level, message = match.groups()
                csv_writer.writerow([timestamp, log_level, message])

# Batch process log files in data folder
log_files = glob.glob('data/*.log')
for log_file in log_files:
    csv_file = log_file.replace('.log', '_processed.csv')

    process_log_to_csv(log_file, csv_file)
    print(f"Processed {log_file} to {csv_file}")

    # Remove rows where log level == warning
    with open(csv_file, 'r') as file:
        lines = file.readlines()

    with open(csv_file, 'w') as file:
        for line in lines:
            if 'warning' not in line.lower():
                file.write(line)
