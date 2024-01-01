import requests
import sys

def requests_handler(url: str, headers: dict={'User-Agent': "WLZ Wachtlijsten dashboard"}) -> requests:
    """
    Deze functie neemt een url en haalt daarmee de API/HTML gegevens op.
    Er wordt automatisch door verschillende user agents gecycled, voornamelijk handig voor webscrapers, het is ook mogelijk om je eigen user agent mee te geven.

    Args:
        url (str): De link naar de website/api endpoint
        user_agent (str, optional): User agent die je wilt meegeven tijdens het GET request Defaults to "".

    Raises:
        Exception: _description_

    Returns:
        requests: Het requests object wordt teruggegeven om er vervolgens mee verder te gaan.
    """
    print(f"Grabbing data from the following url: {url}")
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        # Handles any network-related exceptions
        print(f"An error occurred while fetching the HTML: {e} from {url}")
        print("Check your network settings and try again")
        sys.exit(1)
    
def extract_text_from_html(html):
    try:
        html_text = html.text.strip()
        return html_text
    except AttributeError as err:
        print(err)
        return None