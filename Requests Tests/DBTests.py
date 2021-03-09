import requests
import json

if __name__ == "__main__":
    with open ("./config.json") as f:
        authKey = json.load(f)["secretKey_API"]
    r = requests.get("http://127.0.0.1:5000/api/admin/token.json",
        headers = {
            "authKey": authKey,
            "discordUUID": "90",
            "discordTag": "newi"
            }
        )
    if r.status_code == 200 and "token" in (r_responseJSON := json.loads(r.text)):
        s = requests.post("http://127.0.0.1:5000/api/submit.json",
            data = {
                "fsp_auth_token": r_responseJSON["token"],
                "fsp_coordinate_x": "127",
                "fsp_coordinate_y": "0",
                "fsp_anonymise": "public",
                "fsp_colourId": "15622397"
            }
        )
        if s.status_code == 200:
            print(s.text)
        else:
            print(s.status_code)
    else:
        print(r.status_code)
        try:
            print(r.text)
        except:
            pass
