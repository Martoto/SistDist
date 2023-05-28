from datetime import datetime
import time
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
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

@app.get('/login')
def login_get():
    return  

api.add_resource(LeilaoApiHandler, '/flask/leilao')

class LoginForm(FlaskForm):
    User_Acc = StringField(validators=[InputRequired(), Length(min=2, max=255)], render_kw={"placeholder" : "Usuario", "class": "form-control form-control-user"})
    
    User_Password = PasswordField(validators=[InputRequired(), Length(min=4, max=255)], render_kw={"placeholder" : "Senha", "class": "form-control form-control-user"})
    
    submit = SubmitField("Entrar", render_kw={"class": "btn btn-primary btn-user btn-block"})


if __name__ == '__main__':
        mercado = mercadoLeiloes()

        # enter the service loop.
        scheduler = BackgroundScheduler()
        scheduler.add_job(mercado.atualizarLista, 'interval', seconds=1)
        scheduler.start()
        print("Servidor do Mercado de Leilões aberto")
