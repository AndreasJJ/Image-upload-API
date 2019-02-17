# @author Andreas Jensen Jonassen

# @description Imports
from flask import render_template, request, flash, redirect, url_for, send_from_directory, g
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import uuid, os, re, json, shortuuid
from shutil import move
from host import app, db
from host.models import User
from host.models import link

# @description Allowed file extensions and function to check, for the file upload.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

###########
# Routing #
###########

# Index routing
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# Dashboard routing
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/overview.html', page="Home", username=current_user.username , profile_picture="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solid_white.svg/2000px-Solid_white.svg.png")

# Dashboard routing
@app.route('/dashboard/links')
@login_required
def dashboard_links():
    links = []
    for link in current_user.links.limit(20):
        links.append(link.url)
    return render_template('dashboard/links.html', page="Images", links=links, username=current_user.username , profile_picture="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solid_white.svg/2000px-Solid_white.svg.png")

@app.route('/dashboard/upload')
@login_required
def dashboard_upload():
    return render_template('dashboard/upload.html', page="Upload", username=current_user.username , profile_picture="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solid_white.svg/2000px-Solid_white.svg.png")

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
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        # Get credentials from form
        username = request.form['username']
        password = request.form['password']
        # Get user from database
        try:
            user = User.query.filter_by(username=username).first()
        except exc.IntegrityError:
            flash('Database Error, Please Try Again Later', 'error')
            return redirect(url_for('login'))
        # Check if user exists and if correct password
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'error')
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
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    # If POST Request => Register
    if request.method == 'POST':
        # Check if the form contains the required credentials
        if("username" not in request.form or "password" not in request.form or "confirm_password" not in request.form):
            flash('Username, Password and Confirmation Password was not supplied.', 'error')
            return redirect(url_for('register'))
        # Get the credentials
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Validates the credentials and either registers them or sends an error.
        if(validate_form(username, password, confirm_password)):
            user = User.query.filter_by(username=username).first()
            # Check if user exists
            if user is not None:
                flash('That Username Is Taken. Try Another', 'error')
                return redirect(url_for('register'))
            try:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
            except exc.IntegrityError:
                session.rollback()
                flash('Database Error, Please Try Again Later', 'error')
                return redirect(url_for('register'))
            # Flash confirmation of registration
            flash('Congratulations, you are now a registered user!', 'info')
            # Redirect to login after registration
            return redirect(url_for('login'))
        else:
            # Flash error
            flash(get_form_validation_error(username, password, confirm_password), 'error')
            # Redirect them back to register
            return redirect(url_for('register'))
    else:
        return render_template('register/register.html')
    
# Form validation function
def validate_form(username, password, confirm_password):
    if (password != confirm_password):
        return False
    if (len(username) < 3 or len(username) > 16):
        return False
    if (len(password) < 6 or len(password) > 32):
        return False
    if (not bool(re.match("^[A-Za-z0-9_-]*$", username))):
        return False
    if (not bool(re.match(r"[A-Za-z0-9@#$%^&+=]{6,}", password))):
        return False
    return True

def get_form_validation_error(username, password, confirm_password):
    if (password != confirm_password):
        return "Password and Confirmation Password Did Not Match"
    if (len(username) < 3 or len(username) > 16):
        return "The Username Length is Not Between 3 and 16 characters"
    if (len(password) < 6 or len(password) > 32):
        return "The Passwprd Length is Not Between 6 and 32 characters"
    if (not bool(re.match("^[A-Za-z0-9_-]*$", username))):
        return "The Username Can Only Contain Alphabetic Characters, Hyphens or Underscore"
    if (not bool(re.match(r"[A-Za-z0-9@#$%^&+=]{6,}", password))):
        return "The Password Contained An Illegal Character or Was Shorter Than 6 Characters"
    return None

# API for getting various information about the user.
@app.route('/api', methods=['GET', 'POST'])
def api():
    if(current_user.is_authenticated):
        user = current_user
    elif("username" in request.form or "password" in request.form):
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return render_template('errors/401.html'), 401
    else:
        return render_template('errors/401.html'), 401
    # API GET request
    if request.method == 'GET':
        data = request.args.get('data');
        if(data == "storage_space"):
            return json.dumps({'storage_space': user.storage_space })
        if(data == "storage_used"):
            return json.dumps({'used': get_storage_used(user)})
        if(data == "links"):
            start = request.args.get('start');
            end = request.args.get('end');
            if(not start):
                start = 0
            # Handle not giving an end
            if(not end):
                print("test1")
                try:
                    start = int(start)
                except Exception as e:
                    return render_template('errors/400.html'), 400
                _links = user.links.offset(start).all()
                links = []
                for _link in _links:
                    links.append(_link.url)
                return json.dumps({'links': links})
            else:
                print("test2")
                try:
                    start = int(start)
                    end = int(end)
                except Exception as e:
                    return render_template('errors/400.html'), 400
                _links = user.links.limit(end-start).offset(start).all()
                links = []
                for _link in _links:
                    links.append(_link.url)
                return json.dumps({'links': links})
    # API POST request
    if request.method == 'POST':
        operation = request.args.get('operation');
        # If delete request
        if(operation == "delete"):
            # Get the links from the request as json
            filenames = request.get_json()
            # Check if the requester is the owner of the links
            try:
                owned_links_obj = link.query.filter_by(user_id = user.id).filter(link.url.in_(filenames)).all()
                owned_links = []
                for _link in owned_links_obj:
                    owned_links.append(_link.url)
                # Delete the links from the database
                link.query.filter(link.url.in_(owned_links)).delete(synchronize_session='fetch')
                db.session.commit()
                # Delete the links from the os file system
                for _link in owned_links:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], _link))
                    except Exception as e:
                        print("TODO ADD ERRO HANDLER")        
                return "Deleted", 200
            except exc.IntegrityError:
                session.rollback()
    return render_template('errors/400.html'), 400

def get_storage_used(user):
    size = 0
    for _link in user.links:
        size += _link.size
    return size

# Upload API for uploading images or videos
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request form contains credentials
    if(not current_user.is_authenticated): 
        if("username" not in request.form or "password" not in request.form):
            return render_template('errors/401.html'), 401

        # Get credentials
        username = request.form['username']
        password = request.form['password']

        # Query to database
        user = User.query.filter_by(username=username).first()
        # Check if user exists and if correct password
        if user is None or not user.check_password(password):
            return render_template('errors/401.html'), 401
        # Check if the request contain a file named file
    else:
        user = current_user

    if 'file' not in request.files:
        flash('No file part')
        return render_template('errors/400.html'), 400
    
    # Get file
    file = request.files['file']
    

    # If file is empty
    if file.filename == '':
        flash('No selected file')
        # TODO REMOVE
        return render_template('errors/400.html'), 400
    # Save file, get uuid filename, get size and save the info in the database
    # Before redirecting them to the image
    if file and allowed_file(file.filename):
        storage = get_storage_used(user)
        if(user.storage_space is not None):
            if(user.storage_space <= storage):
                return render_template('errors/507.html'), 507

        new_filename = str(shortuuid.uuid()) + str(os.path.splitext(secure_filename(file.filename))[1]);
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'tmp', new_filename))
        temp_size = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], 'tmp', new_filename)).st_size

        if(user.storage_space < storage + temp_size):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'tmp', new_filename))
            return render_template('errors/507.html'), 507

        move(os.path.join(app.config['UPLOAD_FOLDER'], 'tmp', new_filename), os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        #Save the file
        size = os.stat(os.path.join(app.config['UPLOAD_FOLDER'],new_filename)).st_size
        #Save link in 
        new_link = link(url=new_filename, user_id=user.id, size=size)
        db.session.add(new_link)
        db.session.commit()
        #Redirect to link to the newly uploaded file
        return redirect(url_for('get_image',filename=new_filename))
    return render_template('errors/400.html'), 400

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
def bad_request(error):
    return render_template('errors/400.html'), 400

# 500 Error handler
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
