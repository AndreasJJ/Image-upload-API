# @author Andreas Jensen Jonassen

# @description Imports
from flask import render_template, redirect, url_for
from host import app

###########
# Routing #
###########

from host.router.pages.dashboard import dashboard_blueprint
from host.router.pages.login import login_blueprint
from host.router.pages.logout import logout_blueprint
from host.router.pages.registration import registration_blueprint
from host.router.pages.api import api_blueprint
from host.router.pages.upload import upload_blueprint
from host.router.pages.get_file import get_file_blueprint

# Index routing
@app.route('/')
def index():
    return redirect(url_for('dashboard.dashboard_index'))

app.register_blueprint(dashboard_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(registration_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(get_file_blueprint)

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
