from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy import func
from host import db
from host.models import link, User
import json

api_blueprint = Blueprint('api', __name__, template_folder='templates')

@api_blueprint.route('/api', methods=['GET', 'POST'])
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

def get_storage_used(_user):
    size = db.session.query(func.sum(link.size)).group_by(link.user_id).filter(_user.id == link.user_id).first()
    if size is not None:
        return size[0]
    else:
        return 0
    