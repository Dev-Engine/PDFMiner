"""."""
import os
import time
import urllib
import json
import xmltodict
from flask import (Flask, request, session, redirect, url_for,
                   render_template, flash, make_response)

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from model.models import db
from model.models import User, Project, PdfEm

UPLOAD_FOLDER = os.path.abspath(os.path.dirname('')) + '/static/pdfs'

ALLOWED_EXTENSIONS = {'pdf'}

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
))

db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """."""
    if request.method == "POST" and "project_name" in request.form:
        username = session['username']
        author = User.objects(name=username).first()

        project_name = request.form['project_name']
        current_project = Project(name=project_name)
        current_project.author = author
        current_project.save()

        return redirect(url_for('home'))
    else:
        try:
            username = session['username']
            author = User.objects(name=username).first()
            projects = Project.objects(author=author).order_by('-created_at')
        except:
            projects = []

        return render_template('home.html', projects=projects)


@app.route('/project_del/<project_id>')
def project_del(project_id):
    """."""
    Project.objects(pk=project_id).first().delete()
    return redirect(url_for('home'))


@app.route('/project/<project_id>')
def project(project_id):
    """."""
    current_project = Project.objects(pk=project_id).first()
    return render_template('project.html', project=current_project)


@app.route('/project_upload', methods=['POST'])
def project_upload():
    """."""
    if request.method == 'POST':
        project_id = request.form['project_id']
        up_file = request.files['pdffile']
        current_project = Project.objects(pk=project_id)

        username = session['username']
        author = User.objects(name=username).first()
        if up_file:
            filename = (secure_filename(up_file.filename) +
                        str(int(time.time())))
            filename = filename.replace('.pdf', '') + '.pdf'
            pdf_em = PdfEm(
                name=filename,
                author=author
            )
            current_project.update_one(push__pdfs=pdf_em)
            up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('project', project_id=project_id))
    return render_template('project.html')


@app.route('/pdf_del/<project_id>/<pdf_name>')
def pdf_del(project_id, pdf_name):
    """."""
    current_project = Project.objects(pk=project_id)
    a = current_project.first()
    for i in a.pdfs:
        if i.name == pdf_name:
            pdf_em = PdfEm(
               name=pdf_name,
               author=i.author,
               created_at=i.created_at
            )
            current_project.update_one(pull__pdfs=pdf_em)
    return redirect(url_for('project', project_id=project_id))


@app.route('/pdf/detail/<pdf_name>')
def pdf_detail(pdf_name):
    """."""
    return render_template('pdf_detail.html', pdf_name=pdf_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """."""
    error = None
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        user = User.objects(name=username).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = username
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/pdf/search', methods=['POST'])
def pdf_search():
    """."""
    if request.method == "POST" and "keywords" in request.form:
        keywords = request.form["keywords"]

        api = "http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?" \
              "jn=" + keywords + "&hc=10&rs=11&sortfield=ti&" \
              "sortorder=asc"

        opener = urllib.FancyURLopener({})
        f = opener.open(api)
        o = xmltodict.parse(f.read())

        response = make_response(json.dumps(o))
        return response


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
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
