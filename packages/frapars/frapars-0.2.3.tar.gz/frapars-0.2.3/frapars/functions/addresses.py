import re
from frapars.functions import clean_str
import frapars.constants.regex as rx
from tqdm import tqdm
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from frapars.models.address_result import AddressResult 
import logging


def score_percentage(text):
    # Calculate the percentage score based on the length of the string
    if len(text) <= 50:
        # If the length is less than or equal to 50, calculate the percentage
        percentage_score = ((50 - len(text)) / 50)
    else:
        # If the length is more than 50, percentage score is 0%
        percentage_score = 1.0
    return percentage_score


def format_details(address_info):
    logging.debug(f"Formatting address details: {address_info}")
    address_str = "{} {} {} {} {} {} {} {}".format(
        (' ').join(address_info.get('addres_num', '')),
        (' ').join(address_info.get('urba_names', '')),
        (' ').join(address_info.get('street_name', '')),
        (' ').join(address_info.get('city', '')),
        (' ').join(address_info.get('postcode', '')),
        (' ').join(address_info.get('insee', '')),
        (' ').join(address_info.get('codes', '')),
        (' ').join(address_info.get('department', '')),
    )
    # Replace multiple spaces with a single space
    address_str = re.sub(r'\s+', ' ', address_str)
    # Capitalize the first letter of each word
    return address_str.title()


def parse_all(addresses_list: List[str]):
    """Parse a list of addresses address. The addresses can be still be formed by more addresses inside. (by mistake)
     Like: 15 rue saint philippe ; 13 rue 4 march

     Args:
         addresses_list (List): list of addresses
     Returns:
         List: the list of parsed
     """
    parsed_addresses = []
    for address in tqdm(addresses_list, desc="Processing", unit="item"):
        parsed_addresses.append(parse(address))
    return parsed_addresses

def process_batch(batch_with_indices: List[tuple]) -> List[tuple]:
    """Process a batch of addresses and return results with their original indices."""
    batch_indices, batch = zip(*batch_with_indices)
    parsed_batch = [AddressResult(address, parse(address)) for address in tqdm(batch, desc="Processing batch", unit="item")]
    return list(zip(batch_indices, parsed_batch))


def parse_all_parallel(addresses_list: List[str], batch_size=5000, n_threads=6) -> List[dict]:
    """Parse a large list of addresses in batches, processing up to n_threads batches concurrently.
    
    Args:
        addresses_list (List[str]): List of addresses to be parsed.
        batch_size (int): Number of addresses per batch.
        n_threads (int): Number of threads to use for batch processing.
        
    Returns:
        List[dict]: List of parsed addresses in the same order as input.
    """
    # Create indexed batches
    logging.debug(f"Setting up {n_threads} threads to process {len(addresses_list)} addresses in batches of {batch_size}...")
    indexed_addresses = list(enumerate(addresses_list))
    batches = [indexed_addresses[i:i + batch_size] for i in range(0, len(indexed_addresses), batch_size)]
    
    parsed_addresses = [None] * len(addresses_list)

    def process_batch_and_collect(batch_with_indices: List[tuple]) -> List[tuple]:
        """Process a batch and collect the results with their original indices."""
        return process_batch(batch_with_indices)

    # Use ThreadPoolExecutor to process batches concurrently
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(process_batch_and_collect, batch) for batch in batches]

        for future in as_completed(futures):
            try:
                # Collect results and place them in the correct order
                results_with_indices = future.result()
                for index, parsed_address in results_with_indices:
                    parsed_addresses[index] = parsed_address
            except Exception as e:
                logging.error(f"An error occurred: {e}")

    return parsed_addresses


def parse(addresses_str, sep='et'):
    """Parse an address. The address can still be formed by more addresses inside. (by mistake) 
    Like: 15 rue saint philippe ; 13 rue 4 march

    Args:
        addresses_str (_type_): address location
        sep (str, optional): char, symbol or sequence of char that  we want as a separator for the final addresses. Defaults to 'et'.

    Returns:
        _type_: parsed single address
    """
    parsed_addresses = []
    # there can be multiple str
    addresses = re.split(r';|\b\s*et\s*\b', addresses_str)
    for address_str in addresses:
        address_str = address_str.strip()
        parsed_addresses.append(parse_single_address(address_str))
    return f' {sep} '.join(parsed_addresses)


def parse_single_address(address_str):
    logging.debug(f"Initial address is: {address_str}")
    addr_details = {}
    # norm_address = clean_str.normalize_text(address_str)
    norm_address = address_str.lower()

    # Find all matches for urban names using the compiled pattern
    addr_details['urba_names'], norm_address = rx.exec(
        rx.urban_names_pattern, norm_address, 'urban names')
    norm_address = norm_address.replace('()', '')

    # Find all matches for city using the compiled pattern
    date_streets, norm_address = rx.exec(
        rx.date_pattern, norm_address, 'date streets')

    # Find all matches for city using the compiled pattern
    addr_details['city'], norm_address = rx.exec(
        rx.city_pattern, norm_address, 'city')

    # Find all matches for postcode using the compiled pattern
    codes, norm_address = rx.exec(
        rx.postal_insee_code_pattern, norm_address, 'codes')
    # find the category of the insee
    if len(codes):
        addr_details['insee'], addr_details['postcode'], addr_details['codes'] = rx.parse_codes(
            codes)

    # Find all matches for address number using the compiled pattern
    addr_details['addres_num'], norm_address = rx.exec(
        rx.address_num_pattern, norm_address, 'address number')

    # Find all matches for address_num using the compiled pattern
    addr_details['department'], norm_address = rx.exec(
        rx.department_pattern, norm_address, 'department')

    # Handle the rest
    addr_details['street_name'], norm_address = rx.exec(
        rx.street_name_pattern, norm_address, 'street name')
    addr_details['street_name'].extend(date_streets)

    parsed_address = format_details(addr_details)
    logging.debug(f"Result is: {parsed_address}")
    logging.debug(f"Details: {addr_details}")
    logging.debug(f"Unparsed string remained is: {norm_address}")
    logging.debug(f"Parse quality scored: {score_percentage(norm_address)}")
    return parsed_address.strip()
