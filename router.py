from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import uuid
import os
import sqlite3
from flask import g

##############
# App Config #
##############

app = Flask(__name__, template_folder="static/")
app.secret_key = 'super-duper-secret-key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

############
# Database #
############

DATABASE = './database/users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

###########
# Routing #
###########

@app.route('/')
def index():
    return render_template('errors/401.html'), 401

@app.route('/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

@app.route('/upload', methods=['POST'])
def upload_file():
    if("username" not in request.form or "password" not in request.form):
        return render_template('errors/401.html'), 401

    username = request.form['username']
    password = request.form['password']

    #Check if the user exists with the username and password provided
    cur = get_db().execute('SELECT username, password FROM users WHERE username=? AND password=?;', (username, password,))
    user = cur.fetchone()
    cur.close()

    if (user is None):
        return render_template('errors/401.html'), 401

    if 'file' not in request.files:
        flash('No file part')
        return 'test1'

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return 'test2'
    if file and allowed_file(file.filename):
        #Get the new filename
        new_filename = str(uuid.uuid4().hex) + str(os.path.splitext(secure_filename(file.filename))[1]);
        #Save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        #Save link in database
        cur = get_db().execute('INSERT INTO links(link, username) VALUES(?,?);', (str(new_filename), str(user[0]),))
        get_db().commit()
        cur.close()
        #Redirect to link to the newly uploaded file
        return redirect(url_for('get_image',filename=new_filename))


##################
# ERROR HANDLERS #
##################

# 404 Error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(401)
def unauthorized_access(error):
    return render_template('errors/401.html'), 401

# 500 Error handler
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
