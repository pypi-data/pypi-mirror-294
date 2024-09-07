import logging
import re
from typing import List, Dict
from enum import Enum

class AddressFields(Enum):
    ADDRESS_NUM = "{address_num}"
    URBA_TYPE = "{urba_names}"
    STREET_NAME = "{street_name}"
    CITY = "{city}"
    POSTCODE = "{postcode}"
    INSEE = "{insee}"
    CODES = "{codes}"
    DEPARTMENT = "{department}"

def _safe_format(template, in_dict):
    for key, value in in_dict.items():
        template = template.replace(f"{{{key}}}", ' '.join(value))
    template = re.sub(r'\{[^\}]*\}', '', template)
    return template

class Formatter:
    DEFAULT_FORMAT = f"{AddressFields.ADDRESS_NUM.value} {AddressFields.URBA_TYPE.value} {AddressFields.STREET_NAME.value} {AddressFields.CITY.value} {AddressFields.POSTCODE.value} {AddressFields.INSEE.value} {AddressFields.CODES.value} {AddressFields.DEPARTMENT.value}"

    def __init__(self, template: str = DEFAULT_FORMAT) -> None:
        self.template = template
    
    def format_all(self, address_info: List[Dict], sep='et') -> str:
        return f' {sep} '.join([self.format(address_part).strip() for address_part in address_info])
    
    def format(self, address_info: Dict) -> str:
        # Replace placeholders with values from address_info
        formatted_address = _safe_format(self.template, address_info)

        logging.debug(f"formatted_address: {formatted_address}")

        # Replace multiple spaces with a single space
        formatted_address = re.sub(r'\s+', ' ', formatted_address)
        # Capitalize the first letter of each word
        return formatted_address.strip().title()

        
