from config import BASE_PATH, USER_AGENT
from utils.webscraping_utils import requests_handler, extract_text_from_html
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import glob
import os
import re
import shutil

def get_pdf_links_and_type(url) -> list:
    response = requests_handler(url)
    soup = BeautifulSoup(response.text, 'lxml')
    alle_pdfs = soup.select('#rapportages-wachtlijstinformatie-instellingsniveau a')

    list_of_pdfs = []

    for pdf in alle_pdfs:
        soort_pdf = extract_text_from_html(pdf.select_one('h4'))
        link_naar_pdf = pdf['href']

        list_of_pdfs.append([soort_pdf, link_naar_pdf])
    
    return list_of_pdfs

def extract_specific_text(input_text):
    pattern = r'Cijfers\s(.*?)(?:\s\w+)?\s\d{4}'
    match = re.search(pattern, input_text)

    if match:
        result = match.group(1)
        return result
    else:
        print("No match found.")

def extract_and_create_date(text: str) -> str:
    month_name = text.split()[-2]  # Assuming the month name is the fourth word
    year = int(text.split()[-1][0:4])

    month_dict = {'januari': 1, 'februari': 2, 'maart': 3, 'april': 4, 'mei': 5, 'juni': 6,
              'juli': 7, 'augustus': 8, 'september': 9, 'oktober': 10, 'november': 11, 'december': 12}
    
    month = month_dict.get(month_name.lower())
    date_object = str(datetime(year, month, 1))

    return date_object[:10]

def get_pdfs(list_of_pdf_links: list, base_url) -> None:
    for pdf in list_of_pdf_links:
        url = base_url + pdf[1]
        type_zorg_wachtlijst = extract_specific_text(pdf[0])
        name_of_pdf = extract_and_create_date(pdf[0]) + ' ' + type_zorg_wachtlijst+'.pdf'
        
        response = requests_handler(url)
        print(name_of_pdf)

        with open(name_of_pdf, "wb") as file:
            file.write(response.content)

def load_pdfs_to_raw(path):
    
    pdf_files = glob.glob(f'{path}/*.pdf')
    for pdf in pdf_files:
        file_name = os.path.basename(pdf)
        destination = os.path.join(path+'Raw', file_name)
        shutil.move(pdf, destination)

def main():
    
    # Deze variabele wordt in de code hergebruikt.
    BASE_URL = 'https://www.zorgcijfersdatabank.nl'

    url_van_wachtlijstinformatie = BASE_URL+"/toelichting/wachtlijstinformatie/wachtlijsten-instellingsniveau"
    
    pdfs = get_pdf_links_and_type(url_van_wachtlijstinformatie)
    get_pdfs(pdfs, BASE_URL)
    load_pdfs_to_raw(BASE_PATH)
    
if __name__ == '__main__':
    main()