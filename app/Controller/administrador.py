from flask import Blueprint, render_template, request, redirect, send_from_directory, current_app
from flaskext.mysql import MySQL
import os
from datetime import datetime
from flask import Flask

app = Flask(__name__)

mysql = MySQL()
administrador_blueprint = Blueprint('administrador', __name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

@administrador_blueprint.record_once
def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA

@administrador_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)

@administrador_blueprint.route('/vista')
def index():
    try:
        sql = "SELECT * FROM administrador;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        administrador = cursor.fetchall()
        conn.commit()

        return render_template('/Dashboard-Admin/administrador/index.html', administrador=administrador)  
    except Exception as e:
        print("Error al ejecutar la consulta SQL:", str(e))
        return "Error al cargar los datos. Por favor, inténtalo de nuevo más tarde."

@administrador_blueprint.route('/destroy/<int:Admin_Id>')
def destroy(Admin_Id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Admin_Foto FROM administrador WHERE Admin_Id=%s", Admin_Id)
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

        cursor.execute("DELETE FROM administrador WHERE Admin_Id=%s", (Admin_Id))
        conn.commit()
        return redirect('/administrador/vista')
    except Exception as e:
        print("Error al eliminar el administrador:", str(e))
        return "Error al eliminar el administrador. Por favor, inténtalo de nuevo más tarde."

@administrador_blueprint.route('/edit/<int:Admin_Id>')
def edit(Admin_Id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM administrador WHERE Admin_Id=%s", (Admin_Id))
        administrador = cursor.fetchall()
        conn.commit()

        return render_template('Dashboard-Admin/administrador/edit.html', administrador=administrador)
    except Exception as e:
        print("Error al cargar los datos del administrador:", str(e))
        return "Error al cargar los datos del administrador. Por favor, inténtalo de nuevo más tarde."

@administrador_blueprint.route('/update', methods=['POST'])
def update():
    try:
        _Admin_Nombre = request.form['AdNombre']
        _Admin_Correo = request.form['AdCorreo']
        _Admin_Foto = request.files['AdFoto']
        _Admin_Id = request.form['AdID']

        sql = "UPDATE `administrador` SET Admin_Nombre=%s, Admin_Correo=%s WHERE Admin_Id=%s;"
        datos = (_Admin_Nombre, _Admin_Correo, _Admin_Id)

        conn = mysql.connect()
        cursor = conn.cursor()

        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")

        if _Admin_Foto.filename != '':
            nuevoNombreFoto = tiempo + _Admin_Foto.filename
            _Admin_Foto.save("uploads/" + nuevoNombreFoto)

            cursor.execute("SELECT Admin_Foto FROM administrador WHERE Admin_Id=%s", _Admin_Id)
            fila = cursor.fetchall()

            os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
            cursor.execute("UPDATE administrador SET Admin_Foto=%s WHERE Admin_Id=%s", (nuevoNombreFoto, _Admin_Id))
            conn.commit()

        cursor.execute(sql, datos)
        conn.commit()

        return redirect('/administrador/vista')
    except Exception as e:
        print("Error al actualizar el administrador:", str(e))
        return "Error al actualizar el administrador. Por favor, inténtalo de nuevo más tarde."

@administrador_blueprint.route('/create')
def create():
    return render_template('Dashboard-Admin/administrador/create.html')

@administrador_blueprint.route('/store', methods=['POST'])
def storage():
    _Admin_Nombre = request.form['AdNombre']
    _Admin_Correo = request.form['AdCorreo']
    _Admin_Foto = request.files['AdFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _Admin_Foto.filename != '':
        nuevoNombreFoto = tiempo + _Admin_Foto.filename
        _Admin_Foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `administrador` (`Admin_Id`, `Admin_Nombre`, `Admin_Correo`, `Admin_Foto`) VALUES (NULL, %s, %s, %s);"

    datos = (_Admin_Nombre, _Admin_Correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/administrador/vista')
