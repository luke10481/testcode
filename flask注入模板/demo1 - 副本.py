import flask
import urllib
from flask import Flask
import os
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template("127.0.0.1.html")

if __name__ == '__main__':
    app.run(debug=True)