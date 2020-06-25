from application import app, session, users, socketio, emit, flash, render_template, request, redirect, url_for
from flask import jsonify
from models.chat import *

AllMessages = [
    Message('nico', 'juan', 'Hola Juan'), 
    Message('juan', 'nico', 'Hola Nico'), 
    Message('nico', 'juan', 'soy nico'),
    Message('nico', 'nico', 'Este es un mensaje conmigo mismo')
]

@app.route('/chat', methods=['GET', 'POST'])
def login():
    # GET
    if request.method == "GET":
        if session['activeUser']:
            return render_template('logged/chat.html')

        return redirect(url_for('index'))

    # POST
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        if username == '':
            flash("You must enter your username to login", 'danger')
            return redirect(url_for('index'))

        try:
            if username != session['username']:
                i = 0
                found = False
                while i < len(users) and not found:
                    if users[i] == session['username']:
                        users.pop(i)
                        found = True
                    i += 1
        except KeyError:
            print('error')
            redirect('before_first_request')

        if username not in users:
            users.append(username)

        session['username'] = username
        session['activeUser'] = True
        return render_template('logged/chat.html')


@socketio.on('fetch users')
def fetchUsers():
    data = {}
    data['username'] = session['username']
    data['users'] = users
    emit('users', data, broadcast=True)


@socketio.on('submit message')
def message(data):
    if data['message']:
        idSender = session['username']
        idReceiver = data['receiver']
        message = data['message']
        message = Message(idSender, idReceiver, message)
        AllMessages.append(message)
        emit('message submitted', message, broadcast=True)


@app.route('/fetchMessages', methods=['POST'])
def fetchMessages():
    idReceiver = request.form['idReceiver']
    obj = {}
    messages = []

    for msg in AllMessages:
        if (msg.idSender == session['username'] and msg.idReceiver == idReceiver) or (msg.idSender == idReceiver and msg.idReceiver == session['username']):
            messages.append(msg.__dict__)

    obj['messages'] = messages
    return jsonify(obj)
