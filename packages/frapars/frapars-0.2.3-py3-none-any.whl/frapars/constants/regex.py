
import re
from frapars.constants.words import prepositions, urban_type, months
from frapars.constants.france_deps import get_deps
from frapars.functions.file_parser import parse_insee_file
import logging

logging.debug("Initializing data for the parse")
insee_list, postcode_list, city_list = parse_insee_file()

logging.debug("Compiling usefull regexes")
special_chars_with_apostrophe = r'[^a-zA-Z0-9\s\']'

# Sort by length to prioritize longer matches
urba_type_sorted = sorted(urban_type, key=len, reverse=True)
prepositions_sorted = sorted(prepositions, key=len, reverse=True)
# Create the regex pattern 
urba_type_pattern = "|".join(map(re.escape, urba_type_sorted))
prepositions_pattern = "|".join(map(re.escape, prepositions_sorted))
# Combine the urba_type with optional prepositions
urban_names_pattern = re.compile(
    rf"\b(?:{urba_type_pattern})(?:\s+(?:{prepositions_pattern}))?\b", flags=re.IGNORECASE)

# Define a regular expression pattern to match five consecutive digits
postal_insee_code_pattern = re.compile(r'\b\d{5}\b')

# Regular expression for capturing address numbers, including possible variations like "bis," "b," "a," etc.,
# address_num_pattern = re.compile(
#     r'\b(\d+(?:\s?-\s?\d+|\s?à\s?\d+)?(?:\s?(?:bis|Bis|BIS))?(?:/\d+)?[a-zA-Z]?)\b'
# )
address_num_pattern = re.compile(
    r'\b\d+(?:\s?[-à]\s?\d+)?(?:\s?bis)?(?:/\d+)?[a-zA-Z]?\b'
)


# Regular expression pattern to match cities
city_pattern = re.compile(
    r'\b(?:' + '|'.join(map(re.escape, city_list)) + r')\b', flags=re.IGNORECASE)

# Regular expression pattern to match department names
department_pattern = re.compile(
    r'\b(?:' + '|'.join(map(re.escape, get_deps())) + r')\b', flags=re.IGNORECASE)

street_name_pattern = re.compile(
    r'\b[A-Za-zÀ-ÿ- ]+\b')

date_pattern = re.compile(
    r'\b(?:\d{{1,2}}\s+)?(?:{})\s+\d{{4}}\b'.format('|'.join(months)))


def parse_codes(codes):
    insee = []
    postcode = []
    unknow = []
    for code in codes:
        if code in insee_list and code in postcode_list:
            unknow.append(code)
        elif code in insee_list:
            insee.append(code)
        elif code in postcode_list:
            postcode.append(code)
        else:
            unknow.append(code)
    return insee, postcode, unknow


def exec(pattern, text, lable=None):
    try:
        logging.debug(f"Examining {text}. Looking for {lable}")
        # Find all departments in the input string
        results = pattern.findall(text)
        # Find all matches and remove them from the text
        remaining_text, _ = re.subn(pattern, '', text)
        # Replace multiple spaces with a single space
        remaining_cleaned_text = re.sub(r'\s+', ' ', remaining_text)
        # return the items found and the cleaned str
        return results, remaining_cleaned_text.strip()
    except Exception as e:
        logging.error(f"Error in parsing: {text}. Caused by: {e}")
        return [], text
