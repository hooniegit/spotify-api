
# create access token for spotify
def get_acccess_token(cnt):
    import os
    from configparser import ConfigParser

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(current_dir, f'../config/config.ini')

    parser = ConfigParser()
    parser.read(config_dir)
    access_token = parser.get("SPOTIFY", f"access_token_{cnt}")
    return access_token


# send request to spotify API & get response 
def get_response(cnt, endpoint, params:dict=None):
    import os, sys, requests
    from datetime import datetime

    nowdate = datetime.now().strftime("%Y-%m-%d")
    nowtime = datetime.now().strftime("%H:%M:%S")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    error_dir = os.path.join(current_dir, f'../log/request/{nowdate}.error')

    access_token = get_acccess_token(cnt)
    url = f"https://api.spotify.com/v1/{endpoint}"
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    if params != None:
        response = requests.get(url=url, params=params, headers=headers)
    else:
        response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        error = f"KEY-{cnt}: ERROR APPEARED: {nowtime}: {response.status_code} \n"
        try:
            with open(error_dir, "a") as file:
                file.write(error)
        except:
            with open(error_dir, "w") as file:
                file.write(error)      
        print("ERROR APEEARED")      
        sys.exit()


# test
if __name__ == "__main__":
    # confirmed - 23.10.16
    endpoint = 'browse/new-releases'
    params = {
        'limit': '50',
        'offset': '0',
    }
    response = get_response(cnt=1, endpoint=endpoint, params=params)
    print(response)