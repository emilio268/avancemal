# __init__.py

from flask import Flask
from flaskext.mysql import MySQL
from .config.config import Config
from .config.configure_database import configure_database
from .Controller.Controller import empleados_blueprint, clientes_blueprint
from .Controller.login import login_blueprint
from .routes import route

app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
app.secret_key = "VelaDanAik123"

configure_database(app)

app.register_blueprint(empleados_blueprint)
app.register_blueprint(clientes_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(route)
