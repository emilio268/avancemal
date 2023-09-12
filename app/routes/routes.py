from flask import render_template, request, session, Blueprint, redirect, url_for
from flask_mysqldb import MySQL

route = Blueprint('route', __name__)

mysql = MySQL()


@route.route('/')
def inicio():
    return render_template('/index.html')

@route.route('/login')
def mostrar_login():

    return render_template('login/login.html')

@route.route('/dashboard-proyectos')
def mostrar_dashboardproyectos():

    return render_template('/Dashboard-Admin/proyectos/index.html')

@route.route('/dashboard-srv-create')
def mostrar_dashboardservicioscreate():

    return render_template('/Dashboard-Admin/servicios/create.html')

@route.route('/dashboard-emp-list')
def mostrar_dashboardemplist():

    return render_template('/Dashboard-Admin/empleados/index.html')

@route.route('/dashboard-proy-create')
def mostrar_dashboardproycreate():

    return render_template('/Dashboard-Admin/proyectos/create.html')

@route.route('/dashboard-admin')
def mostrar_dashboardadmin():

    return render_template('/Dashboard-Admin/admin_Dashboard.html')

@route.route('/dashboard-clie')
def mostrar_dashboardemple():

    return render_template('/Dashboard-Admin/clientes/index.html')

@route.route('/dashboard-clie-create')
def mostrar_dashboardemplecreate():

    return render_template('/Dashboard-Admin/clientes/create.html')

@route.route('/dashboard-emp')
def mostrar_dashboardemp():

    return render_template('/Dashboard-Empleado/index.html')

@route.route('/dashboard-cli')
def mostrar_dashboardcli():

    return render_template('/Dashboard-Cliente/Clie-Dashboard.html')

@route.route('/dashboard-emp-create')
def mostrar_dashboardempcreate():

    return render_template('/Dashboard-Admin/empleados/create.html')

@route.route('/admin-chat')
def mostrar_adminchat():

    return render_template('/Dashboard-Admin/chat.html')

@route.route('/admin-profile')
def mostrar_adminedit():

    return render_template('/Dashboard-Admin/administrador/edit.html')

@route.route('/logout')
def logout():
    session.clear()
    return render_template('/index.html')

if __name__== '__main__':
    route.run(debug=True)