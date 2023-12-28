import requests
import json

def extract(url: str) -> json:
    """
    Deze functie bevraagt de API van de Iwlz standaarden: https://modules.istandaarden.nl/tabelbeheer.
    De data die opgehaald wordt is de zorgaanbiederslijst. De gehele lijst wordt meegenomen, maar niet de historie van individuele records.

    Args:
        url (string): 

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    headers = {
    'Accept': 'application/json',
    'User-Agent': 'Wachtlijsten dashboard (jespervanbeemdelust@hotmail.com)'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print(response.text)
        return response.json()
    else:
        raise Exception
        print(f"API kan niet bevraagd worden, de volgende statuscode is ontvangen {response.status_code}")

def load_raw(response_data, file_path):

    with open(file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=2)

def main():

    # Url van de API
    base_url = "https://modules.istandaarden.nl/tabelbeheer/public/api/zorgaanbieders?showActiveOnly=false"

    # Locatie van de json gegevens confrom standaard: brons/raw
    raw_locatie = 'C:\Code\dashboard_projects\wlz_wachtlijsten\Tabellen\DIM_Zorgaanbieder\Raw\Zorgaanbieders_istandaarden.json'
    json_data = extract(base_url)

    load_raw(json_data, raw_locatie)

if __name__ == "__main__":
    main()