import os, requests
from configparser import ConfigParser

current_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(current_dir, f'../../config/config.ini')

parser = ConfigParser()
parser.read(config_dir)

for cnt in range (1, 6):
    client_id = parser.get("SPOTIFY", f"client_id_{cnt}")
    client_sc = parser.get("SPOTIFY", f"client_sc_{cnt}")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_sc}'.encode()
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()

    access_token = response['access_token']

    parser.set('SPOTIFY', f'access_token_{cnt}', access_token)
    with open(config_dir, 'w') as configfile:
        parser.write(configfile)


# confirmed - 23.10.16