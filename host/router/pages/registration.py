from flask import Blueprint, render_template, flash, request, redirect, url_for
from host import db
from host.models import User
from flask_login import current_user
import re

registration_blueprint = Blueprint('registration', __name__, template_folder='../../templates')

@registration_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    # If POST Request => Register
    if request.method == 'POST':
        # Check if the form contains the required credentials
        if("username" not in request.form or "password" not in request.form or "confirm_password" not in request.form):
            flash('Username, Password and Confirmation Password was not supplied.', 'error')
            return redirect(url_for('register.register'))
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
                return redirect(url_for('registration.register'))
            try:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
            except exc.IntegrityError:
                session.rollback()
                flash('Database Error, Please Try Again Later', 'error')
                return redirect(url_for('registration.register'))
            # Flash confirmation of registration
            flash('Congratulations, you are now a registered user!', 'info')
            # Redirect to login after registration
            return redirect(url_for('login.login'))
        else:
            # Flash error
            flash(get_form_validation_error(username, password, confirm_password), 'error')
            # Redirect them back to register
            return redirect(url_for('registration.register'))
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