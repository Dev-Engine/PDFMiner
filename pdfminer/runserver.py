"""."""
import os
from flask import (Flask, request, session, redirect, url_for,
                   render_template, flash)

from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from model.models import db
from model.models import User

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


@app.route('/')
def home():
    """."""
    return render_template('home.html')


@app.route('/project/<project_id>')
def project(project_id):
    """."""
    return render_template('project.html')


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
