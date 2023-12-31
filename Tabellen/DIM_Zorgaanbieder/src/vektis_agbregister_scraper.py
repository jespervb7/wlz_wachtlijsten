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
import pandas as pd

def get_agbcodes() -> list:
    pass

def find_soup_and_extract(agbcode: str, headers: dict):

    response = requests_handler(f'https://www.vektis.nl/agb-register/vestiging-{agbcode}', headers)
    soup = BeautifulSoup(response.text, 'lxml')
    controle_pagina = soup.select_one('h1.title.title--h1.mb-3')

    if controle_pagina == None:
        soort_agb = "Vestiging"
        agb_data = extract_data_vestiging(soup, soort_agb, agbcode)
    else:
        response = requests_handler(f'https://www.vektis.nl/agb-register/onderneming-{agbcode}', headers)

    return agb_data

def extract_data_vestiging(soup_object: BeautifulSoup, soort_agb: str, agbcode: str):
    # Basis registratie gegevens
    dict_basis_registratie = {}
    basisregistratie_html = soup_object.select("div.data-stack.basic-info__pair")

    for column in basisregistratie_html:
        column_name = extract_text_from_html(column.select_one("div.data-stack__label"))
        column_value = extract_text_from_html(column.select_one("div.data-stack__value"))
        
        dict_basis_registratie[column_name] = column_value

    onderneming_link = soup_object.select_one("td.card-table-table__cell a")['href']
    onderneming_agb = onderneming_link[-8:]

    data_basis_registratie = [agbcode, soort_agb, onderneming_agb, dict_basis_registratie]

    # Adres gegevens
    adresgegevens_html = soup_object.select("div.contact-block.contact-block--is-address div.row.my-n3 div.col-sm-6.col-lg-4.py-3")

    data_adres_gegevens = []

    for column in adresgegevens_html:
        type_adres = extract_text_from_html(column.select_one("h4.title.mb-1"))
        adres = extract_text_from_html(column.select_one("div"))

        data_adres_gegevens.append[agbcode, type_adres, adres]
    
    return data_basis_registratie, data_adres_gegevens
    
def extract_data_onderneming():
    pass

def main():
    #first scrape the vestigingen agbcodes + controle of goede webpagina. Voeg J toe als gescraped anders N.
    #second scrape the ondernemingen.
    x = ["47471602", "30300680"]
    basisregistratie = []
    contact_gegevens = []

    for agb in x:
        random_user_agent = random.choice(USER_AGENTS_LIST)
        header = {'User-Agent': random_user_agent}
        agb_data = find_soup_and_extract(agb, header)
        basisregistratie.append(agb_data[0])
        contact_gegevens.append(agb_data[1])

        # Om de website niet te overbelasten, slaap 5 seconden
        time.sleep(5)
    
    # df aanmaken voor basisregristratie gegevens
    df_basisregristratie_met_dict = pd.DataFrame(basisregistratie, columns=['AGB Code', 'Soort zorgaanbieder', 'Hoort bij onderneming','dict'])
    df_finished_basisregristratie = pd.concat([df_basisregristratie_met_dict.drop('dict', axis=1), df_basisregristratie_met_dict['dict'].apply(pd.Series)], axis=1)
    
    # df aanmaken voor adres gegevens.
    df_finished_adresgegevens = pd.DataFrame(contact_gegevens, columns=['AGB Code', 'Correspondentieadres', 'Bezoekadres'])

    print(df_finished_basisregristratie)
    print(df_finished_adresgegevens)

if __name__ == "__main__":
    main()