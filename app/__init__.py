#!/usr/bin/env python
import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:password@localhost/project2database' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yqleetvfawyszd:ed27d45830a0b8193e034b2985fe45f930d45345dfc76f2bca930c996313cd2d@ec2-54-227-237-223.compute-1.amazonaws.com:5432/dbn3umu53imvq7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
CSRF_ENABLED = True

from app import models

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads/')

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'} 

app.config.from_object(__name__)

from app import views


class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)
        
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

CORS(app)