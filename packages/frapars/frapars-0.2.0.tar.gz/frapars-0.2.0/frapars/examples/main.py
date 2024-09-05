import pandas as pd
import chardet
import csv
from frapars.functions.addresses import parse_all_parallel, parse_all, parse
from frapars.constants import out_file_path as out_csv_path
import importlib.metadata
import argparse
import time
# import ptvsd

version = importlib.metadata.version('frapars')


def print_banner():
    # Read the contents of the banner.txt file
    with open('banner.txt', 'r') as file:
        banner_text = file.read()
    # Replace ${application.version} with the desired version
    banner_text = banner_text.replace('${application.version}', version)
    # Print the modified banner
    print(banner_text)


def csv_from_dict(file_path, data):
    print(f"Storing into file the results")
    # Write the list of dictionaries to a CSV file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print("Result printed at: ", file_path)


def parse_from_file(in_file_path, limit=None):
    # Read the file in binary mode
    with open(in_file_path, 'rb') as file:
        raw_data = file.read()
    # Detect the encoding
    print("Examin input file ...")
    result = chardet.detect(raw_data)
    print(f"Detected encoding: {result['encoding']} with confidence {result['confidence']}")
    df = pd.read_csv(in_file_path, dtype='str', encoding=result['encoding'] if result['confidence'] > 0.7 else 'utf-8')
    df = df.dropna()
    if limit:
        csv_addr_list = list(df['address'])[:limit]
    else:
        csv_addr_list = list(df['address'])

    print(f"Found {len(csv_addr_list)} addresses to parse")
    return parse_all_parallel(csv_addr_list)


def parse_from_list(list_of_addresses):
    #  split the addresses
    addresses = list_of_addresses.split(';')
    # Print each value as list
    return parse_all_parallel(addresses)


def parse_from_address(address_str):
    parse(address_str, verbose=True)


def main():
    start_time = time.time()
    print_banner()
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Example Argument Parser')
    # Create a mutually exclusive group for input options
    input_group = parser.add_mutually_exclusive_group(required=True)

    # Add arguments
    input_group.add_argument('-i', '--input-file',
                             type=str, help='Path to the input file')
    input_group.add_argument('-l', '--list', type=str,
                             help='List of inputs. Needs to be on format "rue saint-Philippe 31; Aevenue Carlos (De) 31"')
    input_group.add_argument('-a', '--address', type=str,
                             help='Single input address. Ex: "rue saint-Philippe 31 (De)"')
    input_group.add_argument('-o', '--output', type=str,
                             choices=['show', 'file'],
                             default='show',
                             help='Output option. Choose "show" to display the result or "file" to store it in a file')

    # Parse the arguments
    args = parser.parse_args()

    # Execute based on the input arg
    if args.input_file:
        result = parse_from_file(args.input_file)
    if args.list:
        print(args.list)
        result = parse_from_list(args.list)
    if args.address:
        result = parse_from_address(args.address)

    if args.output == 'file':
        results = [res.to_dict() for res in  result]
        #  store in the file the data collected
        csv_from_dict(out_csv_path, results)
    else:
        for entry in result:
            print(f"Raw: {entry.raw} --> Formatted: {entry.formatted}")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Process has finished in: {execution_time} seconds")


if __name__ == "__main__":
    main()
