from flask import Flask, flash, Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash

# Crear una instancia de Flask
app = Flask(__name__)
app.secret_key = "VelaDanAik123"

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sistema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistema'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
db = SQLAlchemy(app)

# Blueprint para el login
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'Usua_Correo' in request.form and 'Usua_Pass' in request.form:
        _correo = request.form['Usua_Correo']
        _password = request.form['Usua_Pass']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE Usua_Correo = %s', (_correo,))
        account = cur.fetchone()

        if account is not None:
            session['Usua_Correo'] = _correo
            session['Usua_Pass'] = _password
            session['Usua_Nombre'] = account['Usua_Nombre']
            session['Usua_Id'] = account['Usua_Id']
            session['Usua_Foto'] = account['Usua_Foto']

        if account:
            session['logueado'] = True
            session['Usua_Id'] = account['Usua_Id']
            session['Usua_Rol'] = account['Usua_Rol']
            session['Usua_Foto'] = account['Usua_Foto']

            if session['Usua_Rol'] == 1:
                return render_template("/Dashboard-Admin/admin_Dashboard.html")
            elif session['Usua_Rol'] == 2 :
                return render_template("/Dashboard-Empleado/Emple-Dashboard.html")
            elif session['Usua_Rol'] == 3 :
                return render_template("/Dashboard-Cliente/clie-Dashboard.html")
            elif session['Usua_Rol'] == 4 :
                return render_template("/Dashboard-Empleado/Emple-Dashboard.html")
        else:
            return render_template('index.html', mensaje="Usuario O Contraseña Incorrectas")

    return render_template('/Dashboard-Empleado/Emple-Dashboard.html')

@login_blueprint.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        _correo = request.form['Usua_Correo']
        _contrasena = request.form['Usua_Pass']
        _nombre = request.form['Clie_Nombre']

        cur = mysql.connection.cursor()

        try:
            # Genera un hash seguro de la contraseña
            hashed_password = generate_password_hash(_contrasena).decode('utf-8')

            cur.execute("INSERT INTO usuarios (Usua_Correo, Usua_Pass, Usua_Nombre) VALUES (%s, %s, %s)", (_correo, hashed_password, _nombre))
            mysql.connection.commit()

            Usua_Id = cur.lastrowid

            cur.execute("INSERT INTO clientes (Clie_Nombre, Usua_Id) VALUES (%s, %s)", (_nombre, Usua_Id))
            mysql.connection.commit()

            cur.close()

            flash('Registro exitoso', 'success')
            return redirect(url_for('/login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('login/login.html')

@app.route('/proceso')
def proceso():
    return render_template('')

if __name__== '__main__':
    app.run(debug=True)
