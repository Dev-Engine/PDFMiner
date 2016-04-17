"""."""
import os
from flask import (Flask, request, session, redirect, url_for,
                   render_template, flash)

from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from model.models import db
from model.models import User, Project

UPLOAD_FOLDER = '/Users/tuzii/Develop'
ALLOWED_EXTENSIONS = set(['pdf'])

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """."""
    if request.method == "POST" and "project_name" in request.form:
        username = session['username']
        author = User.objects(name=username).first()

        project_name = request.form['project_name']
        project = Project(name=project_name)
        project.author = author
        project.save()

        return redirect(url_for('home'))
    else:
        username = session['username']
        author = User.objects(name=username).first()
        projects = Project.objects(author=author).order_by('-created_at')

        return render_template('home.html', projects=projects)


@app.route('/project_del/<project_id>')
def project_del(project_id):
    """."""
    Project.objects(pk=project_id).first().delete()
    return redirect(url_for('home'))


@app.route('/project/<project_id>')
def project(project_id):
    """."""
    project = Project.objects(pk=project_id).first()
    return render_template('project.html', project=project)


@app.route('/project_upload', methods=['POST'])
def project_upload():
    """."""
    if request.method == 'POST':
        file = request.files['pdffile']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('project', project_id=1))
    return render_template('project.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """."""
    error = None
    if request.method == "POST" and "username" in request.form:
        username = request.form['username']
        password = request.form["password"]
        user = User.objects(name=username).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = username
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """."""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            user = User(name=username)
            user.password = generate_password_hash(password=password)
            user.save()
        return redirect(url_for('home'))
    return render_template('signup.html', error=error)


@app.route('/logout')
def logout():
    """."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
