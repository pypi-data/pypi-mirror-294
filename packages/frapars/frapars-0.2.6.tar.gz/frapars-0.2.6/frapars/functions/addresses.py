import re
import frapars.constants.regex as rx
from tqdm import tqdm
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from frapars.helper.formatter import Formatter
from frapars.models.address_result import AddressResult


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


def parse_all_parallel(addresses_list: List[str], batch_size=5000, n_threads=6, formatter: Formatter= Formatter()) -> List[dict]:
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

    def process_batch(batch_with_indices: List[tuple], formatter: Formatter= Formatter()) -> List[tuple]:
        """Process a batch of addresses and return results with their original indices."""
        batch_indices, batch = zip(*batch_with_indices)
        parsed_batch = [AddressResult(address, parse(address, formatter)) for address in tqdm(batch, desc="Processing batch", unit="item")]
        return list(zip(batch_indices, parsed_batch))

    # Use ThreadPoolExecutor to process batches concurrently
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(process_batch, batch, formatter) for batch in batches]

        for future in as_completed(futures):
            try:
                # Collect results and place them in the correct order
                results_with_indices = future.result()
                for index, parsed_address in results_with_indices:
                    parsed_addresses[index] = parsed_address
            except Exception as e:
                logging.error(f"An error occurred: {e}")

    return parsed_addresses


def parse(addresses_str, formatter: Formatter= Formatter()):
    """Parse an address. The address can still be formed by more addresses inside. (by mistake) 
    Like: 15 rue saint philippe ; 13 rue 4 march

    Args:
        addresses_str (_type_): address location
        sep (str, optional): char, symbol or sequence of char that  we want as a separator for the final addresses. Defaults to 'et'.

    Returns:
        _type_: parsed single address
    """
    # there can be multiple str
    addresses = re.split(r';|\b\s*et\s*\b', addresses_str)
    return [parse_single_address(address_str, formatter) for address_str in addresses]

def parse_single_address(address_str, formatter: Formatter= Formatter()):
    address_str = address_str.strip()

    addr_details = {
        'raw': address_str,
    }
    # norm_address = clean_str.normalize_text(address_str)
    norm_address = address_str.lower()

    # Find all matches for urban names using the compiled pattern
    urba_type, norm_address = rx.exec(
        rx.urban_type_pattern, norm_address, 'urban names')

    # Find all matches for urban names using the compiled pattern
    urba_preposition, norm_address = rx.exec(
        rx.urba_prepositions_pattern, norm_address, 'urban preposition')
    
    # Check if urba_type is not empty and add it to addr_details
    addr_details['urba_names'] = urba_type + urba_preposition

    norm_address = norm_address.replace('(', '').replace(')', '')

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
        addr_details['insee'], addr_details['postcode'], addr_details['codes'] = rx.parse_codes(codes)

    # Find all matches for address number using the compiled pattern
    addr_details['address_num'], norm_address = rx.exec(
        rx.address_num_pattern, norm_address, 'address number')
    addr_details['address_num'] = ['-'.join(addr_details['address_num'])]

    # Find all matches for address_num using the compiled pattern
    addr_details['department'], norm_address = rx.exec(
        rx.department_pattern, norm_address, 'department')

    # Handle the rest
    addr_details['street_name'], norm_address = rx.exec(
        rx.street_name_pattern, norm_address, 'street name')
    addr_details['street_name'].extend(date_streets)
    
    addr_details['formatted'] = formatter.format(addr_details)

    return addr_details
    
