# Sharex Custom Uploader
A web application for fileupload (specifically for shareX, but works with other clients too, like my mac uploader). The API lets you upload files, get your current storage usage, get your allowed storage usage, delete files, and get all your links. All of the API functions can also be used through the GUI.

# Screenshots
Screenshots can be found on [the wiki](https://github.com/AndreasJJ/ShareX-Custom-Uploader-Host/wiki/Web-User-Interface-Design)

# Browser support
* Newer versions of chrome
* Newer version of firefox

# Tech/framework used

**Application technologies:**
* [Flask](http://flask.pocoo.org/)
  * [Flask-login](https://flask-login.readthedocs.io/en/latest/)
  * [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
  * [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
  * [shortuuid](https://github.com/skorokithakis/shortuuid)
* Sqlite

Flask is our application framework, on which our whole application is running. We also use three modules with it to get additional functionality for login, sql ORM and database migration. We also use a shortuuid for shorter uuid for the file links.

**Deployment technologies:** \
Use my docker container boilerplate for flask applications with https, which can be found [here](https://github.com/AndreasJJ/Flask-https-docker-container-boilerplate) or check out the official flask documentation on how to deploy flask applications.

# Setup Guide
1. Download [my docker boilerplate](https://github.com/AndreasJJ/Flask-https-docker-container-boilerplate) for Flask applications, on a server preferably running ubuntu 18.04 that has docker and docker-compose installed. 
2. Delete the application folder from the docker boilerplate and move the "host" folder from this repo to where you downloaded the docker boilerplate.
3. Replace "from application import app" with "from host import app" in the wsgi.py file from the docker boilerplate.

# Contribute
When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, and follow it in all your interactions with the project.

## Pull Request Process
1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Code of Conduct
This project and everyone participating in it is governed by the Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project leader.

# License
This project is licensed under the GNU Affero General Public License v3.0. It can be found in the root of the repo.
