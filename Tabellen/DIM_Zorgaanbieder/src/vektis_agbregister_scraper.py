"""
Dit script haalt de gegevens van Vektis op bij elke AGB code.
Deze data gebruiken we voor 2 tabellen: DIM_zorgaanbieders en DIM_zorgaanbieder_adres'
Voor de zekerheid hebben we de vestiging en onderneming webpagina's gesplits. 

LETOP! - In het script zit een afhankelijkheid. Het script 'ophalen_agbcodes_wlz.py' moet gerund hebben voordat dit script kan runnen.
TODO: Uitvogelen hoe we dit schedulen met Airflow
"""

from config import BASE_PATH, USER_AGENTS_LIST
from bs4 import BeautifulSoup
from utils.webscraping_utils import requests_handler, extract_text_from_html
import random
import time
import os
import pandas as pd

def get_agbcodes() -> list:
    path_to_json = os.path.join(BASE_PATH, 'Tabellen', 'DIM_Zorgaanbieder', 'Raw', 'Zorgaanbieders_istandaarden.json')
    df = pd.read_json(path_to_json)
    agb_codes = df['agb'].astype(str).str.zfill(8).values

    return agb_codes

def find_soup_and_extract(agbcode: str, headers: dict):

    response = requests_handler(f'https://www.vektis.nl/agb-register/vestiging-{agbcode}', headers)
    soup = BeautifulSoup(response.text, 'lxml')
    controle_juiste_pagina = extract_text_from_html(soup.select_one('h1.title.title--h1 mb-3'))

    if controle_juiste_pagina != "Pagina niet gevonden":
        soort_agb = "Vestiging"
        agb_data = extract_data_vestiging(soup, soort_agb, agbcode)
    else:
        response_onderneming = requests_handler(f'https://www.vektis.nl/agb-register/onderneming-{agbcode}', headers)

        if response_onderneming.status_code == 200:
            soup_onderneming = BeautifulSoup(response_onderneming.text, "lxml")
            soort_agb = 'Onderneming'
            agb_data = extract_data_onderneming(soup_onderneming, soort_agb, agbcode)
        else:
            agb_data = [agbcode, "Onbekend", None, {}]

    return agb_data

def extract_data_vestiging(soup_object: BeautifulSoup, soort_agb: str, agbcode: str):
    # Basis registratie gegevens
    dict_basis_registratie = {}
    basisregistratie_html = soup_object.select("div.data-stack.basic-info__pair")
    
    for column in basisregistratie_html:
        column_name = extract_text_from_html(column.select_one("div.data-stack__label"))
        column_value = extract_text_from_html(column.select_one("div.data-stack__value"))
        
        dict_basis_registratie[column_name] = column_value

    onderneming_link_html = soup_object.select_one("td.card-table-table__cell a")
    if onderneming_link_html != None:
        onderneming_link = onderneming_link_html['href']
        onderneming_agb = onderneming_link[-8:]
    else:
        onderneming_agb = None

    data_basis_registratie = [agbcode, soort_agb, onderneming_agb, dict_basis_registratie]

    # Adres gegevens
    adresgegevens_html = soup_object.select("div.contact-block.contact-block--is-address div.row.my-n3 div.col-sm-6.col-lg-4.py-3")

    data_adres_gegevens = []

    for column in adresgegevens_html:
        type_adres = extract_text_from_html(column.select_one("h4.title.mb-1"))
        adres = extract_text_from_html(column.select_one("div"))

        data_adres_gegevens.append([agbcode, type_adres, adres])
    
    return data_basis_registratie, data_adres_gegevens
    
def extract_data_onderneming(soup_object: BeautifulSoup, soort_agb: str, agbcode: str):
    # Basis registratie gegevens
    dict_basis_registratie = {}
    basisregistratie_html = soup_object.select("div.data-stack.basic-info__pair")

    for column in basisregistratie_html:
        column_name = extract_text_from_html(column.select_one("div.data-stack__label"))
        column_value = extract_text_from_html(column.select_one("div.data-stack__value"))
        
        dict_basis_registratie[column_name] = column_value

    data_basis_registratie = [agbcode, soort_agb, None, dict_basis_registratie]

    # Adres gegevens
    adresgegevens_html = soup_object.select("div.contact-block.contact-block--is-address div.row.my-n3 div.col-sm-6.col-lg-4.py-3")

    data_adres_gegevens = []

    for column in adresgegevens_html:
        type_adres = extract_text_from_html(column.select_one("h4.title.mb-1"))
        adres = extract_text_from_html(column.select_one("div"))

        data_adres_gegevens.append([agbcode, type_adres, adres])
    
    return data_basis_registratie, data_adres_gegevens

def main():
    #first scrape the vestigingen agbcodes + controle of goede webpagina. Voeg J toe als gescraped anders N.
    #second scrape the ondernemingen.
    agb_codes = ['47471602', '30300680', '75753831']
    basisregistratie = []
    adres_gegevens = []

    for agb in agb_codes:
        random_user_agent = random.choice(USER_AGENTS_LIST)
        header = {'User-Agent': random_user_agent,
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.google.com/'}
        agb_data = find_soup_and_extract(agb, header)
        basisregistratie.append(agb_data[0])

        # Omdat we adressen anders ophalen moeten we nu ook door een adres lijst loopen.
        for adres in agb_data[1]:
            adres_gegevens.append(adres)

        # Om de website niet te overbelasten wachten we even per agb
        time.sleep(10)
    print(adres_gegevens)
    # df aanmaken voor basisregristratie gegevens
    df_basisregristratie_met_dict = pd.DataFrame(basisregistratie, columns=['AGB Code', 'Soort zorgaanbieder', 'Hoort bij onderneming','dict'])
    df_finished_basisregristratie = pd.concat([df_basisregristratie_met_dict.drop('dict', axis=1), df_basisregristratie_met_dict['dict'].apply(pd.Series)], axis=1)
    
    # df aanmaken voor adres gegevens.
    df_finished_adresgegevens = pd.DataFrame(adres_gegevens, columns=['AGB Code', 'Soort adres', 'Adres unclean'])

    df_finished_basisregristratie.to_csv("Basisregristratie.csv")
    df_finished_adresgegevens.to_csv("Adresgegevens.csv")

    print(df_finished_basisregristratie)
    print(df_finished_adresgegevens)

if __name__ == "__main__":
    main()