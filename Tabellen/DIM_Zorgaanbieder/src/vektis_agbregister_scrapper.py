"""
Dit script haalt de gegevens van Vektis op bij elke AGB code.
Deze data gebruiken we voor 2 tabellen: DIM_zorgaanbieders en DIM_zorgaanbieder_adres
"""
from config import BASE_PATH
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.vektis.nl/agb-register/onderneming-47471602')
soup = BeautifulSoup(r.text, 'lxml')

controle_pagina = soup.select_one('h1.title.title--h1.mb-3').text.strip()

if controle_pagina == "Pagina niet gevonden":
    print("yes")

def main():
    pass

if __name__ == "__main__":
    main()