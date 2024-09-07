import pandas as pd
import frapars.constants as const
import importlib.resources as pkg_resources
from frapars.constants.insee import insee_list
import frapars.data

# TODO: add update of the insee files!

def get_insee_file():
    # Use importlib.resources to open the CSV file as a resource
    with pkg_resources.open_text(frapars.data, 'insee_file.csv') as file:
        return pd.read_csv(file, delimiter=';', dtype='str', encoding='latin1')


def parse_insee_file():
    df = get_insee_file()
    insee = set(df['#Code_commune_INSEE'])
    sorted_insee_list = sorted(
        insee, key=lambda x: len(x), reverse=True)
    with open('frapars/constants/insee.py', 'w') as file:
        file.write(str(insee))

    # Extract values from the column and cast them into a set
    postcode_list = set(df['Code_postal'])
    sorted_postcode_list = sorted(
        postcode_list, key=lambda x: len(x), reverse=True)
    with open('frapars/constants/postcodes.py', 'w') as file:
        file.write(str(sorted_postcode_list))

    # Extract values from the column and cast them into a set
    nom_commune_list = set(df['Nom_de_la_commune'].str.lower())
    ligne_5_list = set(df['Ligne_5'].dropna().str.lower())

    #  merge the 2
    cities_list = nom_commune_list.union(ligne_5_list)
    sorted_cities_list = sorted(
        cities_list, key=lambda x: len(x), reverse=True)
    with open('frapars/constants/municipalities.py', 'w') as file:
        file.write(str(sorted_cities_list))

    return sorted_insee_list, sorted_postcode_list, sorted_cities_list
