import os
from flask import Flask, request, current_app

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
    DATABASE=os.path.join(app.instance_path, "db.sqlite"),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

import db

db.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
