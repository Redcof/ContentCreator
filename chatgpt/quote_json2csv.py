import json
import csv


def convert_json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as fp:
        # Load the JSON data
        data = json.load(fp)

        # Extract the header from the JSON data
        header = list(data[0].keys())

        # Open the CSV file in write mode
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(header)

            # Write the data rows
            for row in data:
                writer.writerow(row.values())

    print(f"CSV file '{csv_file}' created successfully.")


if __name__ == '__main__':
    convert_json_to_csv('../data_and_config/quotes.json', '../data_and_config/quotes.csv')
