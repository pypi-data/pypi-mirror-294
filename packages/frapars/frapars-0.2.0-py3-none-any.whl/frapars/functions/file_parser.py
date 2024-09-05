import os
import pandas as pd
import requests
import frapars.constants as const

# TODO: add force download if 1moth is passed


def _read_file(url):
    return pd.read_csv(url, delimiter=';', dtype='str', encoding='latin1')


def get_insee_file():
    if os.path.exists(const.insee_path):
        # Load the existing CSV file
        return _read_file(const.insee_path)
    else:
        # Download the CSV file from the URL
        response = requests.get(const.insee_url)
        if response.status_code == 200:
            # Save the downloaded file
            with open(const.insee_path, 'wb') as file:
                file.write(response.content)
            # Load the CSV file into a DataFrame
            return _read_file(const.insee_path)
        else:
            print("Failed to download the file:", response.status_code)
            return None


def parse_insee_file():
    df = get_insee_file()
    # Extract values from the column and cast them into a set and sort by max lenght (for prior in regex)
    insee_list = set(df['#Code_commune_INSEE'])
    sorted_insee_list = sorted(
        insee_list, key=lambda x: len(x), reverse=True)
    # Extract values from the column and cast them into a set
    postcode_list = set(df['Code_postal'])
    sorted_postcode_list = sorted(
        postcode_list, key=lambda x: len(x), reverse=True)
    # Extract values from the column and cast them into a set
    nom_commune_list = set(df['Nom_de_la_commune'].str.lower())
    ligne_5_list = set(df['Ligne_5'].dropna().str.lower())
    cities_list = nom_commune_list.union(ligne_5_list)
    sorted_cities_list = sorted(
        cities_list, key=lambda x: len(x), reverse=True)
    # print(f"Insee list own #{len(insee_list)} values.")
    # print(f"Postcode list own #{len(postcode_list)} values.")
    # print(
    #     f"Common codes list own #{len(insee_list.intersection(postcode_list))} values.")

    return sorted_insee_list, sorted_postcode_list, sorted_cities_list
