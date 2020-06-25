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

users = []

# Routes
@app.before_first_request
def before_first_request():
    session['activeUser'] = False
    session['username'] = None
    
import routes.main
import routes.chat
