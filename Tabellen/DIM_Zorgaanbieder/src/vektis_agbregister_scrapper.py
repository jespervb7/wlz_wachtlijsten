import requests

r = requests.get('https://www.vektis.nl/agb-register/vestiging-47471602')
print(r.text)