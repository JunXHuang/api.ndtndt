"""
Routes and views for the flask application.
"""

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import pypyodbc,json,xmltodict

from ndtndt import app

api = Api(app)
auth = HTTPBasicAuth()

@app.route('/')
@app.route('/home')
def home():
    return jsonify({'status': 'success'})