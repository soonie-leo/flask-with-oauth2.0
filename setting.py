from db import get_db


def getSettings():
    db = get_db()

    logo = db.execute(f"SELECT * FROM logo").fetchone()
    menu = db.execute(f"SELECT * FROM menu").fetchall()
    banner = db.execute(f"SELECT * FROM banner").fetchall()

    return {
        "logo": {"img_link": logo["img_link"]},
        "menu": [
            {"num": m["id"], "title": m["title"], "external_link": m["link"]}
            for m in menu
        ],
        "banner": [
            {
                "num": b["id"],
                "img_link": b["img_link"],
                "external_link": b["external_link"],
                "activate": b["activate"],
            }
            for b in banner
        ],
    }


def updateSettings(data):
    db = get_db()

    # Logo Update
    try:
        if "logo" in data:
            logo = data["logo"]["img_link"]
            db.execute(f"UPDATE logo SET img_link = '{logo}'")
            db.commit()
    except db.Error as e:
        return {"message": f"Error: {e}"}

    # Menu Update
    try:
        if "menu" in data:
            for menu in data["menu"]:
                update_list = []
                if "title" in menu:
                    title = menu["title"]
                    update_list.append(f"title = '{title}'")

                if "external_link" in menu:
                    external_link = menu["external_link"]
                    update_list.append(f"link = '{external_link}'")

                id = menu["num"]

                update_str = ", ".join(update_list)
                print(f"UPDATE menu SET {update_str} WHERE id = {id}")
                db.execute(f"UPDATE menu SET {update_str} WHERE id = {id}")
        db.commit()
    except db.Error as e:
        return {"message": f"Error: {e}"}

    # Banner Update
    try:
        if "banner" in data:
            for banner in data["banner"]:
                update_list = []
                if "img_link" in banner:
                    img_link = banner["img_link"]
                    update_list.append(f"img_link = '{img_link}'")

                if "external_link" in banner:
                    external_link = banner["external_link"]
                    update_list.append(f"external_link = '{external_link}'")

                if "activate" in banner:
                    activate = banner["activate"]
                    update_list.append(f"activate = '{activate}'")

                id = banner["num"]

                update_str = ", ".join(update_list)
                print(f"UPDATE banner SET {update_str} WHERE id = {id}")
                db.execute(f"UPDATE banner SET {update_str} WHERE id = {id}")
        db.commit()
    except db.Error as e:
        return {"message": f"Error: {e}"}

    return {"message": "OK"}
