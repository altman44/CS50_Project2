import os

from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_first_request
def before_first_request():
    session['users'] = list()

@app.route("/")
def index():
    #print(session)
    return render_template('main/home.html')

@app.route('/chat', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        print(session)
        if username == '':
            flash("You must enter your username to login", 'danger')
            return redirect(url_for('index'))
        if username in session['users']:
            flash('That username is already logged in', 'danger')
            return redirect(url_for('index'))

        print(len(session['users']))
        session['users'].append(username)
        print(session)
        return render_template('logged/chat.html')

    return redirect(url_for('index'))
