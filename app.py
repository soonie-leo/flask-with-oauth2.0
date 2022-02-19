import os
from flask import Flask, request, current_app, send_from_directory, url_for
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from threading import Thread
from flask_cors import CORS
from urllib.parse import urlparse

from db import get_db
import oauth
import image
import scripttags
import setting

app = Flask(__name__, instance_relative_config=True, static_url_path="")
app.config.from_mapping(
    SECRET_KEY="dev",
    DATABASE=os.path.join(app.instance_path, "db.sqlite"),
)
CORS(app)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

import db

db.init_app(app)


# 주기적으로 Access Token을 갱신해 줌
# Access Token은 2시간 후 만료되므로, 1시간 50분 마다 갱신한다.

# Thread with app context
class AppContextThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


def batchRefreshToken():
    with app.app_context():
        thread = AppContextThread(
            target=oauth.refreshToken,
        )
        thread.daemon = True
        thread.start()


scheduler = BackgroundScheduler(timezone="Asia/Seoul")
scheduler.add_job(func=oauth.refreshToken, trigger="interval", hours=1, minutes=50)
# scheduler.add_job(func=batchRefreshToken, trigger="interval", minutes=10)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route("/api/token")
def getToken():
    with app.app_context():
        return oauth.getToken()


@app.route("/api/token/refresh", methods=("GET", "POST", "PUT"))
def refreshToken():
    with app.app_context():
        if request.method == "GET":
            return oauth.getToken()

        elif request.method == "POST":
            return oauth.refreshToken()

        elif request.method == "PUT":
            token = request.form["token"]
            expire = request.form["expire"]
            type = request.form["type"]

            if type == "refresh":
                return oauth.updateToken(
                    new_refresh_token=token, new_refresh_token_expire=expire
                )
            else:
                return oauth.updateToken(
                    new_access_token=token, new_access_token_expire=expire
                )


@app.route("/api/image", methods=("GET", "POST"))
def image():
    with app.app_context():
        if request.method == "GET":
            start = int(request.args.get("start", 1))
            display = int(request.args.get("display", 30))
            orderby = request.args.get("orderby", "DESC")
            return image.getImages(start, display, orderby)
        if request.method == "POST":
            img = request.form["image"]
            return image.uploadImage(img)


@app.route("/api/settings", methods=("GET", "PUT"))
def settings():
    with app.app_context():
        if request.method == "GET":
            return setting.getSettings()

        elif request.method == "PUT":
            data = request.get_json()
            print(data)

            return setting.updateSettings()


@app.route("/static/scripttags/<scriptName>")
def getStaticJsFile(scriptName):
    return send_from_directory("scripttags", scriptName)


@app.route("/api/scripttags/<scriptName>")
def script(scriptName):
    src = f"${SERVER_NAME}/static/scripttags/{scriptName}"
    return scripttags.uploadScripttags(src)
