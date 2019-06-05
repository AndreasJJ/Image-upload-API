# @author Andreas Jensen Jonassen

# @description Imports
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# @description Initialization and configuration of the Flask app.
app = Flask(__name__)
app.secret_key = 'super-duper-secret-key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),'uploads')
app.config['MAX_CONTENT_LENGTH'] = 200000000
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('database/database.db') or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# @description Database and Migration system initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# @description Login manager initialization
login = LoginManager(app)
login.login_view = 'login.login'

# @description importing the router and database models
from host.router import router
from host import models

