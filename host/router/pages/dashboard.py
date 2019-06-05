from flask import Blueprint, render_template
from host.models import link
from flask_login import current_user, login_required

dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='../../templates')

@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard_index():
    return render_template('dashboard/overview.html', page="Home", username=current_user.username , profile_picture="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solid_white.svg/2000px-Solid_white.svg.png")

@dashboard_blueprint.route('/dashboard/links')
@login_required
def dashboard_links():
    links = []
    for link in current_user.links.limit(20):
        links.append(link.url)
    return render_template('dashboard/links.html', page="Images", links=links, username=current_user.username , profile_picture="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solid_white.svg/2000px-Solid_white.svg.png")

@dashboard_blueprint.route('/dashboard/upload')
@login_required
def dashboard_upload():
    return render_template('dashboard/upload.html', page="Upload", username=current_user.username , profile_picture="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Solid_white.svg/2000px-Solid_white.svg.png")
