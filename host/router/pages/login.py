from flask import Blueprint, render_template, flash, request, redirect, url_for
from host.models import User
from flask_login import current_user, login_user

login_blueprint = Blueprint('login', __name__, template_folder='../../templates')

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_index'))
    # If POST Request => Logging in
    if request.method == 'POST':
        # Check if post contains form with username and password
        if("username" not in request.form or "password" not in request.form):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login.login'))
        # Get credentials from form
        username = request.form['username']
        password = request.form['password']
        # Get user from database
        try:
            user = User.query.filter_by(username=username).first()
        except exc.IntegrityError:
            flash('Database Error, Please Try Again Later', 'error')
            return redirect(url_for('login.login'))
        # Check if user exists and if correct password
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login.login'))
        # Log in users if everything is correct
        login_user(user, remember=False)
        return redirect(url_for('dashboard.dashboard_index'))
    # Get Request => Requesting login page
    else:
        return render_template('login/login.html')