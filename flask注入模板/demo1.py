import flask
import urllib
from flask import Flask
import os
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template_string("<h1>Index Page</h1>")

@app.route('/hello/<path:name>')
def hello(name):
    return flask.render_template("hello.html", name=name)

@app.errorhandler(404)
def page_not_found(e):
    template = '''
    {%% block body %%}
        <div class="center-content error">
            <h1>Oops!That page doesn't exist.</h1>
            <h3>%s</h3>
        </div>
    {%% endblock %%}
    ''' % (urllib.unquote(flask.request.url))
    return flask.render_template_string(template), 404

if __name__ == '__main__':
    app.run(debug=True)