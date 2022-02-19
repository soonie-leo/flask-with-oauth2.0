from config import API_OAUTH_TOKEN, CLIENT_ID, CLIENT_SECRET

import datetime
import requests
from db import get_db


def refreshToken():
    token_info = getToken()

    url = API_OAUTH_TOKEN
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "refresh_token", "refresh_token": token_info["refresh_token"]}
    res = requests.post(
        url,
        headers=headers,
        data=data,
        auth=(CLIENT_ID, CLIENT_SECRET),
    ).json()

    if "error" in res:
        return {"message": "Error", "data": res}

    new_access_token = res["access_token"]
    new_access_token_expire = res["expires_at"]
    new_refresh_token = res["refresh_token"]
    new_refresh_token_expire = res["refresh_token_expires_at"]

    return updateToken(
        new_access_token,
        new_access_token_expire,
        new_refresh_token,
        new_refresh_token_expire,
    )


def getToken():
    db = get_db()
    token_info = db.execute("SELECT * FROM store").fetchone()

    return token_info


def updateToken(
    new_access_token=None,
    new_access_token_expire=None,
    new_refresh_token=None,
    new_refresh_token_expire=None,
):
    def convertDateFormat(date):
        dateObject = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000")
        return dateObject.strftime("%Y-%m-%d %H:%M:%S")

    updateList = []
    if new_access_token:
        updateList.append('access_token = "' + new_access_token + '"')
    if new_access_token_expire:
        updateList.append(
            'access_token_expire = "' + convertDateFormat(new_access_token_expire) + '"'
        )
    if new_refresh_token:
        updateList.append('refresh_token = "' + new_refresh_token + '"')
    if new_refresh_token_expire:
        updateList.append(
            'refresh_token_expire = "'
            + convertDateFormat(new_refresh_token_expire)
            + '"'
        )

    if len(updateList) > 0:
        updateList.append(
            'modified = "' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '"'
        )
    else:
        return {"message": "Error: wrong parameter."}

    db = get_db()
    try:
        db.execute(f"UPDATE store SET " + ", ".join(updateList))
        db.commit()
    except db.Error as e:
        return {"message": f"Error: {e}"}

    return {"message": "OK"}
