from flask import Blueprint, render_template, request, redirect, send_from_directory, current_app
from flaskext.mysql import MySQL
import os
from datetime import datetime
from flask import Flask
from ..config.configure_database import configure_database

app = Flask(__name__)

configure_database(app)

mysql = MySQL()
mysql.init_app(app)

empleados_blueprint = Blueprint('empleados', __name__)

@empleados_blueprint.record_once
def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA

@empleados_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)

@empleados_blueprint.route('/vista')
def index():
    try:
        sql = "SELECT * FROM empleados;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        empleados = cursor.fetchall()
        conn.commit()

        return render_template('/Dashboard-Admin/empleados/index.html', empleados=empleados)  
    except Exception as e:
        print("Error al ejecutar la consulta SQL:", str(e))
        return "Error al cargar los datos. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/destroy/<int:Emp_Id>')
def destroy(Emp_Id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Emp_Foto FROM empleados WHERE Emp_Id=%s", Emp_Id)
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

        cursor.execute("DELETE FROM empleados WHERE Emp_Id=%s", (Emp_Id))
        conn.commit()
        return redirect('/empleados/vista')
    except Exception as e:
        print("Error al eliminar el empleado:", str(e))
        return "Error al eliminar el empleado. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/edit/<int:Emp_Id>')
def edit(Emp_Id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empleados WHERE Emp_Id=%s", (Emp_Id))
        empleados = cursor.fetchall()
        conn.commit()

        return render_template('Dashboard-Admin/empleados/edit.html', empleados=empleados)
    except Exception as e:
        print("Error al cargar los datos del empleado:", str(e))
        return "Error al cargar los datos del empleado. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/update', methods=['POST'])
def update():
    try:
        _Emp_Nombre = request.form['ENombre']
        _Emp_Correo = request.form['ECorreo']
        _Emp_Foto = request.files['EFoto']
        _Emp_Id = request.form['EID']

        sql = "UPDATE `empleados` SET Emp_Nombre=%s, Emp_Correo=%s WHERE Emp_Id=%s;"
        datos = (_Emp_Nombre, _Emp_Correo, _Emp_Id)

        conn = mysql.connect()
        cursor = conn.cursor()

        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")

        if _Emp_Foto.filename != '':
            nuevoNombreFoto = tiempo + _Emp_Foto.filename
            _Emp_Foto.save("uploads/" + nuevoNombreFoto)

            cursor.execute("SELECT Emp_Foto FROM empleados WHERE Emp_Id=%s", _Emp_Id)
            fila = cursor.fetchall()

            os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
            cursor.execute("UPDATE empleados SET Emp_Foto=%s WHERE Emp_Id=%s", (nuevoNombreFoto, _Emp_Id))
            conn.commit()

        cursor.execute(sql, datos)
        conn.commit()

        return redirect('/empleados/vista')
    except Exception as e:
        print("Error al actualizar el empleado:", str(e))
        return "Error al actualizar el empleado. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/create')
def create():
    return render_template('Dashboard-Admin/empleados/create.html')

@empleados_blueprint.route('/store', methods=['POST'])
def storage():
    _Emp_Nombre = request.form['ENombre']
    _Emp_Correo = request.form['ECorreo']
    _Emp_Foto = request.files['EFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Emp_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Emp_Foto.filename
        _Emp_Foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `empleados` (`Emp_Id`, `Emp_nombre`, `Emp_correo`, `Emp_Foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_Emp_Nombre, _Emp_Correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/empleados/vista')
   
