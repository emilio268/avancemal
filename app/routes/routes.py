from flask import Flask
from flask import render_template,request,redirect,url_for,session, Response, Blueprint
from flask_mysqldb import MySQL,MySQLdb
from flask import send_from_directory
from datetime import datetime

import os

route = Blueprint('route', __name__)


route.secret_key = "VelaDanAik123"

@route.route('/')
def index():
    return render_template('/index.html')

@route.route('/login')
def asd():
    return render_template('/Dashboard-Admin/login.html')

@route.route('/dashboard-admin')
def mostrar_dashboardadmin():

    return render_template('/Dashboard-Admin/admin_Dashboard.html')

#Empleado

@route.route('/dashboard-emple')
def mostrar_dashboardemple():

    return render_template('/Dashboard-Admin/empleados/index.html')

@route.route('/dashboard-emple-create')
def mostrar_dashboardemplecreate():

    return render_template('/Dashboard-Admin/empleados/create.html')

#--------------------------------------------------------------------------------------------

#Cliente

@route.route('/dashboard-clie')
def mostrar_dashboardclie():

    return render_template('/Dashboard-Admin/clientes/index.html')

@route.route('/dashboard-clie-create')
def mostrar_dashboardcliecreate():

    return render_template('/Dashboard-Admin/clientes/create.html')

#--------------------------------------------------------------------------------------------


@route.route('/dashboard-usu')
def mostrar_dashboardusu():

    return render_template('/Dashboard-Usuario/Usuario_Dashboard.html')


@route.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'Usua_Correo' in request.form and 'Usua_Pass' in request.form:
       
        _correo = request.form['Usua_Correo']
        _password = request.form['Usua_Pass']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE Usua_Correo = %s AND Usua_Pass = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['Usua_Id'] = account['Usua_Id']
            session['Usua_Rol'] = account['Usua_Rol']
            
            if session['Usua_Rol']==1:
                return render_template("/Dashboard-Admin/admin_Dashboard.html")
            elif session['Usua_Rol']==2:
                return render_template("admin.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")

route.route('proceso')
def proceso():
    
    return render_template('')

