from typing import List, Dict
class AddressResult:
    def __init__(self, raw, addresses_details: List[Dict]):
        self.raw = raw
        self.formatted = ' et '.join([address['formatted'].strip() for address in addresses_details])
        self.details = addresses_details
    
    def to_dict(self):
        return {
            'raw': self.raw,
            'formatted': self.formatted,
            'details': self.details
        }
    
    def to_string(self):
        return self.formatted