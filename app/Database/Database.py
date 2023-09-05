#modulos que vamos a usar
from flask import Flask
from flask import render_template,request,blueprints,redirect,url_for,session, Response, Blueprint
from flask_mysqldb import MySQL,MySQLdb
from flask import send_from_directory
from datetime import datetime
import os


class database:

    database = Blueprint('empleados', __name__)

    app=Flask(__name__)
    app.secret_key = "VelaDanAik123"

    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'sistema'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql = MySQL(app)



