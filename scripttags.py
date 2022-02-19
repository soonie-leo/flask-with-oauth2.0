from config import API_SCRIPTTAGS
import requests
import oauth


def uploadScripttags(src):
    url = API_SCRIPTTAGS
    headers = {
        "Authorization": "Bearer " + oauth.getToken()["access_token"],
        "Content-Type": "application/json",
        "X-Cafe24-Api-Version": "2021-12-01",
    }
    data = {
        "shop_no": 1,
        "request": {
            "src": src,
            "display_location": ["MEMBER_ADMINFAIL"],
            "exclude_path": [],
            "skin_no": [15],
            "integrity": "sha384-UttGu98Tj02YSyWJ5yU0dHmx4wisywedBShWqEz+TL3vFOCXdeMWmo6jMVR8IdFo",
        },
    }

    res = requests.post(url, headers=headers, json=data).json()
    print(res)

    if "error" in res:
        return {"message": "Error", "data": res}

    return {"message": "OK", "data": res}
