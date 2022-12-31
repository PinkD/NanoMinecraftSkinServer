import os

import flask
from flask import Flask

from db import DB
from util import sha256

app = Flask(__name__)


@app.route('/')
def hello_world():
    return flask.render_template("index.html")


@app.route('/<username>.json')
def get_skin_info(username: str):
    skin = db.get_skin_by_user(username)
    if skin:
        return flask.jsonify(username=username, skin=skin)
    else:
        return flask.jsonify()


@app.route('/textures/<sha>')
def get_skin(sha: str):
    return flask.send_file(f"{skin_prefix}/{sha}", mimetype="image/png")


@app.route('/upload', methods=("POST",))
def upload():
    username = flask.request.form["username"]
    skin = flask.request.files["skin"]
    if username is None or len(username) == 0 or skin is None:
        return flask.abort(400)
    skin = skin.read()
    sha = sha256(skin)
    with open(f"{skin_prefix}/{sha}", "wb") as f:
        f.write(skin)
    update = db.insert_skin(username, sha)
    if update:
        return f"Skin for {username} updated, id is {sha}"
    else:
        return f"Skin for {username} uploaded, id is {sha}"


if __name__ == '__main__':
    db = DB()
    skin_prefix = "skins"
    if not os.path.exists(skin_prefix):
        os.mkdir(skin_prefix)
    if os.path.exists(skin_prefix) and not os.path.isdir(skin_prefix):
        print(f"directory to save skins is not a directory: {skin_prefix}")
        exit(-1)
    app.run(host="0.0.0.0", port=80)
    # app.run(port=80, debug=True)
