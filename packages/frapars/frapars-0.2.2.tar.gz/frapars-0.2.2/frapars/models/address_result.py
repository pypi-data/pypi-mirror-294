class AddressResult:
    def __init__(self, raw, formatted):
        self.raw = raw
        self.formatted = formatted
    
    def to_dict(self):
        return {
            'raw': self.raw,
            'formatted': self.formatted
        }
    
    def to_string(self):
        return self.formatted