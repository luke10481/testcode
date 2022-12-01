from flask import Flask, render_template, redirect, url_for, request, session, abort, flash, make_response

from app import app

@app.route('/')
def index():
        response = make_response(render_template("index.html"))
        return response

@app.route('/reg')
def do_reg():
    return render_template('do_register.html')
