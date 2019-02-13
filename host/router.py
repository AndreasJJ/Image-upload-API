from flask import render_template, request, flash, redirect, url_for, send_from_directory, g
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import uuid, os, re
from host import app, db
from host.models import User, link

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###########
# Routing #
###########

# Index routing. Returns 401 Access denied.
@app.route('/')
def index():
    return render_template('errors/401.html'), 401

# Dashboard routing
@app.route('/dashboard')
@login_required
def dashboard():
    return ''

# Login routing
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    # If POST Request => Logging in
    if request.method == 'POST':
        # Check if post contains form with username and password
        if("username" not in request.form or "password" not in request.form):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Get credentials from form
        username = request.form['username']
        password = request.form['password']
        # Get user from database
        user = User.query.filter_by(username=username).first()
        # Check if user exists and if correct password
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Log in users if everything is correct
        login_user(user, remember=False)
        return redirect(url_for('dashboard'))
    # Get Request => Requesting login page
    else:
        return render_template('login/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Register routing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if("username" not in request.form or "password" not in request.form or "confirm_password" not in request.form):
            flash('Invalid username or password')
            return redirect(url_for('register'))
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if(validate_form(username, password, confirm_password)):
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            print("test2")
            return redirect(url_for('register'))
    else:
        return render_template('register/register.html')
    

def validate_form(username, password, confirm_password):
    print(username, password, confirm_password)
    if (password != confirm_password):
        print("error1")
        return False
    if (len(username) < 3 or len(username) > 16):
        print("error2")
        return False
    if (len(password) < 6 or len(password) > 32):
        print("error3")
        return False
    if (not bool(re.match("^[A-Za-z0-9_-]*$", username))):
        print("error4")
        return False
    if (not bool(re.match(r"[A-Za-z0-9@#$%^&+=]{6,}", password))):
        print("error5")
        return False
    return True

# Upload API for uploading images or videos
@app.route('/upload', methods=['POST'])
def upload_file():
    if("username" not in request.form or "password" not in request.form):
        return render_template('errors/401.html'), 401

    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    # Check if user exists and if correct password
    if user is None or not user.check_password(password):
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
        size = os.stat(os.path.join(app.config['UPLOAD_FOLDER'],new_filename)).st_size
        #Save link in 
        new_link = link(url=new_filename, user_id=user.get_id(), size=size)
        db.session.add(new_link)
        db.session.commit()
        #Redirect to link to the newly uploaded file
        return redirect(url_for('get_image',filename=new_filename))
    
# Routing for images
@app.route('/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

##################
# ERROR HANDLERS #
##################

# 404 Error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# 401 Error handler
@app.errorhandler(401)
def unauthorized_access(error):
    return render_template('errors/401.html'), 401

# 404 Error handler
@app.errorhandler(400)
def not_found_error(error):
    return render_template('errors/400.html'), 400

# 500 Error handler
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
