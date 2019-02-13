from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__, template_folder="static/")
app.secret_key = 'super-duper-secret-key'

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200000000

############
# Database #
############
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('database/database.db') or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from host import router, models
