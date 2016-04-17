"""."""
import os
from flask import (Flask, request, session, redirect, url_for,
                   render_template, flash)

from werkzeug import secure_filename

from model.models import db

UPLOAD_FOLDER = '/Users/tuzii/Develop'
ALLOWED_EXTENSIONS = set(['pdf'])

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    PASSWORD='admin'
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
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """."""
    error = None
    if request.method == 'POST':
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
