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

clientes_blueprint = Blueprint('clientes', __name__)

@clientes_blueprint.record_once
def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA

@clientes_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)

@clientes_blueprint.route('/vista')
def index():
    try:
        sql = "SELECT * FROM clientes;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        clientes = cursor.fetchall()
        conn.commit()

        return render_template('/Dashboard-Admin/clientes/index.html', clientes=clientes)    
    except Exception as e:
        print("Error al ejecutar la consulta SQL:", str(e))
        return "Error al cargar los datos. Por favor, inténtalo de nuevo más tarde."

@clientes_blueprint.route('/destroy/<int:Clie_Id>')
def destroy(Clie_Id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Clie_Foto FROM clientes WHERE Clie_Id=%s", Clie_Id)
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

        cursor.execute("DELETE FROM clientes WHERE Clie_Id=%s", (Clie_Id))
        conn.commit()
        return redirect('/clientes/vista')
    except Exception as e:
        print("Error al eliminar el cliente:", str(e))
        return "Error al eliminar el cliente. Por favor, inténtalo de nuevo más tarde."

@clientes_blueprint.route('/edit/<int:Clie_Id>')
def edit(Clie_Id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE Clie_Id=%s", (Clie_Id))
        clientes = cursor.fetchall()
        conn.commit()

        return render_template('/Dashboard-Admin/clientes/edit.html', clientes=clientes)
    except Exception as e:
        print("Error al cargar los datos del cliente:", str(e))
        return "Error al cargar los datos del cliente. Por favor, inténtalo de nuevo más tarde."

@clientes_blueprint.route('/update', methods=['POST'])
def update():
    try:
        _Clie_Nombre = request.form['CNombre']
        _Clie_Correo = request.form['CCorreo']
        _Clie_Foto = request.files['CFoto']
        _Clie_Id = request.form['CID']

        sql = "UPDATE `clientes` SET Clie_Nombre=%s, Clie_Correo=%s WHERE Clie_Id=%s;"
        datos = (_Clie_Nombre, _Clie_Correo, _Clie_Id)

        conn = mysql.connect()
        cursor = conn.cursor()

        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")

        if _Clie_Foto.filename != '':
            nuevoNombreFoto = tiempo + _Clie_Foto.filename
            _Clie_Foto.save("uploads/" + nuevoNombreFoto)

            cursor.execute("SELECT Clie_Foto FROM clientes WHERE Clie_Id=%s", _Clie_Id)
            fila = cursor.fetchall()

            os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
            cursor.execute("UPDATE clientes SET Clie_Foto=%s WHERE Clie_Id=%s", (nuevoNombreFoto, _Clie_Id))
            conn.commit()

        cursor.execute(sql, datos)
        conn.commit()

        return redirect('/clientes/vista')
    except Exception as e:
        print("Error al actualizar el cliente:", str(e))
        return "Error al actualizar el cliente. Por favor, inténtalo de nuevo más tarde."

@clientes_blueprint.route('/create')
def create():
    return render_template('/Dashboard-Admin/clientes/create.html')

@clientes_blueprint.route('/store', methods=['POST'])
def storage():
    _Clie_Nombre = request.form['CNombre']
    _Clie_Correo = request.form['CCorreo']
    _Clie_Foto = request.files['CFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Clie_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Clie_Foto.filename
        _Clie_Foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `clientes` (`Clie_Id`, `Clie_nombre`, `Clie_Correo`, `Clie_Foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_Clie_Nombre, _Clie_Correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/clientes/vista')
