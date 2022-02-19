from config import API_PRODUCTS_IMAGES
from db import get_db
import oauth
import requests


def uploadImage(image):
    url = API_PRODUCTS_IMAGES
    headers = {
        "Authorization": "Bearer " + oauth.getToken()["access_token"],
        "Content-Type": "application/json",
        "X-Cafe24-Api-Version": "2021-12-01",
    }
    data = {"requests": [{"image": image}]}
    res = requests.post(url, headers=headers, json=data).json()

    if "error" in res:
        return {"message": "Error", "data": res}

    for img in res["images"]:
        addImage(img["path"])

    return {"message": "OK", "data": res}


def getImages(start, display, orderby):
    db = get_db()
    images = db.execute(
        f"SELECT * FROM image ORDER BY created {orderby} LIMIT {start - 1}, {display}"
    ).fetchall()

    return {"message": "OK", "data": images}


def addImage(path):
    db = get_db()
    try:
        db.execute(f"INSERT INTO image (path) VALUES ('{path}')")
        db.commit()
    except db.Error as e:
        return {"message": f"Error: {e}"}

    return {"message": "OK"}
