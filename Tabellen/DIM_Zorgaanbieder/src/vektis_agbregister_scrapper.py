"""
Dit script haalt de gegevens van Vektis op bij elke AGB code.
Deze data gebruiken we voor 2 tabellen: DIM_zorgaanbieders en DIM_zorgaanbieder_adres'

LETOP! - In het script zit een afhankelijkheid. Het script 'ophalen_agbcodes_wlz.py' moet gerund hebben voordat dit script kan runnen.
TODO: Uitvogelen hoe we dit schedulen met Airflow
"""
from config import BASE_PATH, USER_AGENTS_LIST
from bs4 import BeautifulSoup
from utils.webscraping_utils import requests_handler
import requests

def get_controle_html(url):
    response = requests_handler(url)
    soup = BeautifulSoup(response.text, 'lxml')
    controle_pagina = soup.select_one('h1.title.title--h1.mb-3').text.strip()

    return controle_pagina,soup

def find_and_add_soup(agb_lijst: list):

    agb_lijst_to_return = []

    for agbcode in agb_lijst:

        controle_vestiging_url = get_controle_html(f'https://www.vektis.nl/agb-register/vestiging-{agbcode}')

        if controle_vestiging_url[0] != "Pagina niet gevonden":
            agb_lijst_to_return.append([agbcode, controle_vestiging_url[1]])
            continue
        
        controle_onderneming_url = get_controle_html(f'https://www.vektis.nl/agb-register/vestiging-{agbcode}')

        if controle_vestiging_url[0] != "Pagina niet gevonden":
            agb_lijst_to_return.append([agbcode, controle_onderneming_url[1]])
            continue
        else:
            agb_lijst_to_return.append(agbcode, None)
        
    return agb_lijst_to_return


def main():
    base_url = 'https://www.vektis.nl/agb-register/'
    #first scrape the vestigingen agbcodes + controle of goede webpagina. Voeg J toe als gescrapped anders N.
    #second scrape the ondernemingen.
    x = ["47471602", "30300680"]
    y = find_and_add_soup(x)
    for item in y:
        print(item[0])
    

if __name__ == "__main__":
    main()