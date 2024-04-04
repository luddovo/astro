#!/usr/bin/env python3

from wsgiref.handlers import CGIHandler
from flask import render_template
from flask import Flask

app = Flask(__name__, template_folder='.')
@app.route('/')
def index():
    return render_template(
        '_index.html'
    )


@app.route('/suburl')
def index2():
    return '<h1>Hello World 2!</h1>'

CGIHandler().run(app)