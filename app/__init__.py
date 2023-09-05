from flask import Flask
from flask import render_template,request,redirect,url_for,session, Response, Blueprint
from config import Config
from .Database.Database import database
from .routes import route
from .Controller.empleados import empleados_blueprint
from .Controller.clientes import clientes_blueprint


app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPALTE_FOLDER)
app.config.from_object(Config)
app.config.from_object(database)

app.register_blueprint(route)
app.register_blueprint(empleados_blueprint)
app.register_blueprint(clientes_blueprint)



