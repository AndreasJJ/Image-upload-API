from flask import Blueprint, render_template, flash, request, redirect, url_for
from host import db, app
from host.models import User
from host.models import link
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import uuid, os, shortuuid
from shutil import move

upload_blueprint = Blueprint('upload', __name__, template_folder='../../templates')

@upload_blueprint.route('/upload', methods=['POST'])
@login_required
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
        
        if(user.storage_space is not None):
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
        return redirect(url_for('get_file.get_image',filename=new_filename))
    return render_template('errors/400.html'), 400

# @description Allowed file extensions and function to check, for the file upload.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_storage_used(user):
    size = 0
    for _link in user.links:
        size += _link.size
    return size