import requests
import json

if __name__ == "__main__":
    with open ("./config_private.json") as f:
        authKey = json.load(f)["secretKey_API"]
    r = requests.get("http://127.0.0.1:5000/api/token.json",
        headers = {
            "authKey": authKey,
            "discordUUID": "99999",
            "discordTag": "hithere#9000"
            }
        )
    if r.status_code == 200:
        print(r.text)
