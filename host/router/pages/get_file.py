from flask import Blueprint, render_template, send_from_directory
from host import app

get_file_blueprint = Blueprint('get_file', __name__, template_folder='../../templates')

@get_file_blueprint.route('/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)