from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, flash, redirect, url_for, Response, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
from mercadoLeiloes import mercadoLeiloes
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user, user_accessed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, ValidationError
from api.LeilaoApiHandler import LeilaoApiHandler


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
api = Api(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')
     
api.add_resource(LeilaoApiHandler, '/flask/leilao')

