from flask import Blueprint, render_template
from flask_login import logout_user, login_required

logout_blueprint = Blueprint('logout', __name__, template_folder='../../templates')

@logout_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))