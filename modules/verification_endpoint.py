import flask
import json

with open("configs/config.json", "r") as config:
    global app
    app = flask.Flask(json.load(config)['name'])


@app.route("/")
def default():
    return """HELLOWORLD"""