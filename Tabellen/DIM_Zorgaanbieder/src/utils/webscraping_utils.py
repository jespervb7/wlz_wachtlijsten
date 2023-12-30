import requests
import random
from .. config import USER_AGENTS_LIST

def requests_handler(url: str, user_agent: str="") -> requests:
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

    # Determines if the user passed a specific user agent to use. Otherwise use a list of random user agents.
    if user_agent == "":
        selected_user_agent = random.choice(USER_AGENTS_LIST)
    else:
        selected_user_agent = user_agent

    headers = {'User-Agent': selected_user_agent}
    response = requests.get(url, headers=headers)   

    if response.status_code == 200:
        return response
    #TODO: add logger, more statuscode handling/accepting
    else:
        raise Exception(f"API request failed. Status code: {response.status_code}. Response: {response.text}")
    