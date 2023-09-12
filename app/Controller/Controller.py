from flask import Blueprint, render_template, request, redirect, send_from_directory, current_app
from flaskext.mysql import MySQL
import os
from flask import Flask
from datetime import datetime
from ..config.configure_database import configure_database

app = Flask(__name__)

configure_database(app)

empleados_blueprint = Blueprint('empleados', __name__)
clientes_blueprint = Blueprint('clientes', __name__)

def on_load(state):
    global CARPETA
    CARPETA = os.path.join('uploads')
    state.app.config['CARPETA'] = CARPETA

@empleados_blueprint.route('/uploads/<nombreFoto>')
@clientes_blueprint.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    carpeta = current_app.config['CARPETA']
    return send_from_directory(current_app.config['CARPETA'], nombreFoto)

@empleados_blueprint.route('/vista')
@clientes_blueprint.route('/vista')
def index():
    try:
        sql_emp = "SELECT * FROM empleados;"
        sql_cli = "SELECT * FROM clientes;"
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        if request.blueprint == 'empleados':
            cursor.execute(sql_emp)
            data = cursor.fetchall()
        else:
            cursor.execute(sql_cli)
            data = cursor.fetchall()
        
        conn.commit()

        return render_template('/Dashboard-Admin/empleados/index.html' if request.blueprint == 'empleados' else '/Dashboard-Admin/clientes/index.html', data=data)
    except Exception as e:
        print("Error al ejecutar la consulta SQL:", str(e))
        return "Error al cargar los datos. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/destroy/<int:Emp_Id>')
@clientes_blueprint.route('/destroy/<int:Clie_Id>')
def destroy(Emp_Id=None, Clie_Id=None):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        if request.blueprint == 'empleados':
            cursor.execute("SELECT Emp_Foto FROM empleados WHERE Emp_Id=%s", Emp_Id)
        else:
            cursor.execute("SELECT Clie_Foto FROM clientes WHERE Clie_Id=%s", Clie_Id)
        
        fila = cursor.fetchall()

        os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))

        if request.blueprint == 'empleados':
            cursor.execute("DELETE FROM empleados WHERE Emp_Id=%s", (Emp_Id))
        else:
            cursor.execute("DELETE FROM clientes WHERE Clie_Id=%s", (Clie_Id))
        
        conn.commit()
        
        return redirect('/empleados/vista' if request.blueprint == 'empleados' else '/clientes/vista')
    except Exception as e:
        print(f"Error al eliminar el {'empleado' if request.blueprint == 'empleados' else 'cliente'}:", str(e))
        return f"Error al eliminar el {'empleado' if request.blueprint == 'empleados' else 'cliente'}. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/edit/<int:Emp_Id>')
@clientes_blueprint.route('/edit/<int:Clie_Id>')
def edit(Emp_Id=None, Clie_Id=None):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        if request.blueprint == 'empleados':
            cursor.execute("SELECT * FROM empleados WHERE Emp_Id=%s", (Emp_Id))
        else:
            cursor.execute("SELECT * FROM clientes WHERE Clie_Id=%s", (Clie_Id))
        
        data = cursor.fetchall()
        conn.commit()

        return render_template('/Dashboard-Admin/empleados/edit.html' if request.blueprint == 'empleados' else '/Dashboard-Admin/clientes/edit.html', data=data)
    except Exception as e:
        print(f"Error al cargar los datos del {'empleado' if request.blueprint == 'empleados' else 'cliente'}:", str(e))
        return f"Error al cargar los datos del {'empleado' if request.blueprint == 'empleados' else 'cliente'}. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/update', methods=['POST'])
@clientes_blueprint.route('/update', methods=['POST'])
def update():
    try:
        if request.blueprint == 'empleados':
            _Emp_Nombre = request.form['ENombre']
            _Emp_Correo = request.form['ECorreo']
            _Emp_Foto = request.files['EFoto']
            _Emp_Id = request.form['EID']

            sql = "UPDATE `empleados` SET Emp_Nombre=%s, Emp_Correo=%s WHERE Emp_Id=%s;"
            datos = (_Emp_Nombre, _Emp_Correo, _Emp_Id)
        else:
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

        if _Emp_Foto.filename != '' if request.blueprint == 'empleados' else _Clie_Foto.filename != '':
            nuevoNombreFoto = tiempo + (_Emp_Foto.filename if request.blueprint == 'empleados' else _Clie_Foto.filename)
            (_Emp_Foto if request.blueprint == 'empleados' else _Clie_Foto).save("uploads/" + nuevoNombreFoto)

            if request.blueprint == 'empleados':
                cursor.execute("SELECT Emp_Foto FROM empleados WHERE Emp_Id=%s", _Emp_Id)
            else:
                cursor.execute("SELECT Clie_Foto FROM clientes WHERE Clie_Id=%s", _Clie_Id)
                
            fila = cursor.fetchall()

            os.remove(os.path.join(current_app.config['CARPETA'], fila[0][0]))
            if request.blueprint == 'empleados':
                cursor.execute("UPDATE empleados SET Emp_Foto=%s WHERE Emp_Id=%s", (nuevoNombreFoto, _Emp_Id))
            else:
                cursor.execute("UPDATE clientes SET Clie_Foto=%s WHERE Clie_Id=%s", (nuevoNombreFoto, _Clie_Id))
            conn.commit()

        cursor.execute(sql, datos)
        conn.commit()

        return redirect('/empleados/vista' if request.blueprint == 'empleados' else '/clientes/vista')
    except Exception as e:
        print(f"Error al actualizar el {'empleado' if request.blueprint == 'empleados' else 'cliente'}:", str(e))
        return f"Error al actualizar el {'empleado' if request.blueprint == 'empleados' else 'cliente'}. Por favor, inténtalo de nuevo más tarde."

@empleados_blueprint.route('/create')
@clientes_blueprint.route('/create')
def create():
    return render_template('/Dashboard-Admin/empleados/create.html' if request.blueprint == 'empleados' else '/Dashboard-Admin/clientes/create.html')

@empleados_blueprint.route('/store', methods=['POST'])
@clientes_blueprint.route('/store', methods=['POST'])
def storage():
    try:
        if request.blueprint == 'empleados':
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
        else:
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

        return redirect('/empleados/vista' if request.blueprint == 'empleados' else '/clientes/vista')
    except Exception as e:
        print(f"Error al almacenar el {'empleado' if request.blueprint == 'empleados' else 'cliente'}:", str(e))
        return f"Error al almacenar el {'empleado' if request.blueprint == 'empleados' else 'cliente'}. Por favor, inténtalo de nuevo más tarde."

