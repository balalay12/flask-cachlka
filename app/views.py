from flask import render_template
from flask import request, abort
from flask_restful import Resource
from app import app
from app.forms import *
import json


@app.route('/')
def index():
    return render_template('main.html')


class Registration(Resource):
    def post(self):
        data = json.loads(request.data.decode())
        print(data.get('reg'))
        return {'ok': 'ok'}, 200
