from application import app, session, users, socketio, emit, flash, render_template, request, redirect, url_for
from flask import jsonify
from models.chat import *

@app.route('/chat', methods=['GET', 'POST'])
def login():
    sessionKeys = session.keys()

    if 'activeUser' in sessionKeys and 'username' in sessionKeys and 'currentUsernameReceiver' in sessionKeys:
        if session['activeUser']:
            return render_template('logged/chat.html')
    else:
        redirect('before_first_request')

    # GET
    if request.method == "GET":
        return redirect(url_for('index'))

    # POST
    if request.method == 'POST':
        username = request.form['username']
        if username == '':
            flash("You must enter your username to login", 'danger')
            return redirect(url_for('index'))

        # try:
        #     if username != session['username']:
        #         userFound = chat.searchUser(session['username'])
        #         if users[i] == session['username']:
        #             chat.deleteUser()
        # except KeyError:
        #     print('error')
        #     redirect('before_first_request')

        if not users.searchUserByUsername(username):
            users.appendUser(username)
        chatCreated = users.appendChat([username, username])

        chatCreated.submitMessage(username, username, "Hola")
        chatCreated.submitMessage(username, username, "Buenas")

        session['username'] = username
        session['activeUser'] = True
        session['currentUsernameReceiver'] = username
        return render_template('logged/chat.html')

@socketio.on('fetch users')
def fetchUsers():
    data = {}
    data['username'] = session['username']
    data['users'] = users.getUsersUsernames()
    emit('users', data, broadcast=True)

@socketio.on('submit message')
def message(data):
    print(session)
    usernameReceiver = session['currentUsernameReceiver']
    message = data['message']

    if message and usernameReceiver:
        submitted = False
        dataMessage = {}

        usernameSender = session['username']
        usersChat = [usernameSender, usernameReceiver]
        print(f"sender: {usernameSender} y receiver: {usernameReceiver}")
        chatFound = users.searchChatByUsernames(usersChat)

        if chatFound:
            submitted = chatFound.submitMessage(usernameSender, usernameReceiver, message)
        else:
            newChat = users.appendChat(usersChat)
            if newChat:
                submitted = newChat.submitMessage(usernameSender, usernameReceiver, message)
        
        dataMessage['usernameSender'] = usernameSender
        dataMessage['usernameReceiver'] = usernameReceiver
        dataMessage['message'] = message
        print(dataMessage)
        emit('message submitted', dataMessage, broadcast=True)

@app.route('/fetchMessages', methods=['POST'])
def fetchMessages():
    usernameSender = session['username']
    usernameReceiver = request.form['usernameReceiver']
    session['currentUsernameReceiver'] = usernameReceiver

    usersChat = [usernameSender, usernameReceiver]
    chat = users.searchChatByUsernames(usersChat)
    chatSerialized = {}
    if chat:
        chatSerialized = chat.serialize()
    print(session)
    print('chat: ', chatSerialized)
    return jsonify(chatSerialized)

@app.route('/searchUsername', methods=['POST'])
def searchCurrentUsername():
    return session['username']

@app.route('/searchCurrentUsernameReceiver', methods=['POST'])
def searchCurrentUsernameReceiver():
    return session['currentUsernameReceiver']