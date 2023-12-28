from config import BASE_PATH, USER_AGENT
import requests
import os
import json

def extract(url: str) -> json:
    """
    Deze functie bevraagt de API van de Iwlz standaarden: https://modules.istandaarden.nl/tabelbeheer.
    De data die opgehaald wordt is de zorgaanbiederslijst. De gehele lijst wordt meegenomen, maar niet de historie van individuele records.

    Args:
        url (string): URL van de API.

    Raises:
        Exception: API request failed with the given status code.

    Returns:
        json: JSON-gegevens van de API-respons.
    """

    headers = {
    'Accept': 'application/json',
    'User-Agent': USER_AGENT
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print(response.text)
        return response.json()
    else:
        raise Exception(f"API request failed. Status code: {response.status_code}. Response: {response.text}")


def load_raw(response_data: json, file_path: str) -> None:
    """
    Slaat de ruwe JSON-gegevens op in een bestand.

    Args:
        response_data (json): JSON-gegevens om op te slaan.
        file_path (str): Bestandspad waarin de gegevens moeten worden opgeslagen.
    """
    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=2)

def main():
    # Url van de API
    base_url = "https://modules.istandaarden.nl/tabelbeheer/public/api/zorgaanbieders?showActiveOnly=false"

    # Locatie van de json gegevens confrom standaard: brons/raw
    raw_locatie = os.path.join(BASE_PATH, 'Tabellen', 'DIM_Zorgaanbieder', 'Raw', 'Zorgaanbieders_istandaarden.json')
    json_data = extract(base_url)

    load_raw(json_data, raw_locatie)

if __name__ == "__main__":
    main()