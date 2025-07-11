import json
import re
import requests

def extract_server_data(data: str) -> dict:
    match = re.search(r'var\s+ServerData=(.*?);', data)
    return json.loads(match.group(1)) if match else None

def main():
        session = requests.Session()

        emailprimary = ""
        recovery_code = ""

        response = session.post("https://login.live.com")
        cookie_jar = session.cookies
        print(cookie_jar)
        r = session.get(f"https://account.live.com/ResetPassword.aspx?wreply=https://login.live.com/oauth20_authorize.srf&mn={emailprimary}", cookies=cookie_jar)
        cookiess = r.cookies
        amsc = cookiess.get('amsc')

        server_data = extract_server_data(r.text)
        if server_data:
            print("Server data extracted!")
        else:
            print("Server data not found!")

        x = server_data["sRecoveryToken"]
        y = server_data['apiCanary']

        data = {
            "code": recovery_code,
            "recoveryCode": recovery_code,
            "scid": 100103,
            "token": server_data["sRecoveryToken"],
            "uiflvr": 1001,
            "publicKey": "25CE4D96CB3A09A69CD847C69FC6D40AF4A4DE12",
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            "Cookie": f"amsc={amsc}",
            "Content-Type": "application/json; charset=utf-8",
            "canary": server_data['apiCanary']
        }

        r = session.post("https://account.live.com/API/Recovery/VerifyRecoveryCode", data=json.dumps(data), headers=headers, cookies=cookie_jar)
        print(r.text)

        apiCanary = r.json()["apiCanary"]
        token = r.json()["token"]

        data = {
            "contactEmail": "email@email.com",
            "contactEpid": "",
            "password": "sdw34qcf!!cacasdfcCC",
            "passwordExpiryEnabled": 0,
            "scid": 100103,
            "token": token,
        }

        r = scraper.post("https://account.live.com/API/Recovery/RecoverUser", data=json.dumps(data), cookies=cookie_jar, headers=headers)
        c = r.text
        response_dict = json.loads(c)
        print(c)
        recoveryCodenew = response_dict.get("recoveryCode")
        print(recoveryCodenew)
main()
