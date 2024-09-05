import re
from frapars.constants.regex import special_chars_with_apostrophe


def remove_special_characters(text):
    return re.sub(special_chars_with_apostrophe, '', text)


def remove_punctuation_characters(text):
    return text.replace('-', ' ')


def normalize_text(str_address):
    no_puntaction_addr = remove_punctuation_characters(str_address)
    return no_puntaction_addr.lower()
