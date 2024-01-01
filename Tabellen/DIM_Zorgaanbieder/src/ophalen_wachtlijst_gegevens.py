from config import BASE_PATH, USER_AGENT
from utils.webscraping_utils import requests_handler, extract_text_from_html
from bs4 import BeautifulSoup
import requests
import os
import re

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
        print(result)
    else:
        print("No match found.")

def main():
    base_url = 'https://www.zorgcijfersdatabank.nl'
    url_van_wachtlijstinformatie = base_url+"/toelichting/wachtlijstinformatie/wachtlijsten-instellingsniveau"
    
    pdfs = get_pdf_links_and_type(url_van_wachtlijstinformatie)
    x = extract_specific_text(pdfs[0][0])

if __name__ == '__main__':
    main()