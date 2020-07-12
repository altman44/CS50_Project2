import os

from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
from flask_session import Session
from models.chat import Users

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = Users()

# Routes
@app.before_first_request
def before_first_request():
    session['activeUser'] = False
    session['username'] = None
    session['currentUsernameReceiver'] = None
    print(session)
    
import routes.main
import routes.chat
