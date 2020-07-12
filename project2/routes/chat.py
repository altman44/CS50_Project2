from application import app, session, users, socketio, emit, flash, render_template, request, redirect, url_for, join_room
from flask import jsonify
from models.chat import *

@app.route('/chat', methods=['GET', 'POST'])
def login():
    sessionKeys = session.keys()
    if 'activeUser' in sessionKeys and 'username' in sessionKeys and 'currentReceiverUsername' in sessionKeys:
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
            users.addUser(username)
        createdChat = users.addChat([username, username])

        createdChat.submitMessage(username, username, "Por este chat podés enviarte mensajes a vos mismo")

        session['username'] = username
        session['activeUser'] = True
        session['currentReceiverUsername'] = ""
        # print('route chat: ', session)
        return render_template('logged/chat.html')

@socketio.on('fetch users')
def fetchUsers():
    data = {}
    data['username'] = session['username']
    data['users'] = users.getUsersUsernames()
    emit('users', data, broadcast=True)

@socketio.on('submit message')
def message(data):
    #print(session)
    #usernameReceiver = session['currentReceiverUsername']
    receiverUsername = data['currentUsernameReceiver']
    message = data['message']

    print("Submitting msg: " + receiverUsername)

    if message and receiverUsername:
        submitted = False
        dataMessage = {}

        senderUsername = session['username']
        usersChat = [senderUsername, receiverUsername]
        print(f"sender: {senderUsername} y receiver: {receiverUsername}")
        chatFound = users.searchChatByUsernames(usersChat)

        if chatFound:
            submitted = chatFound.submitMessage(senderUsername, receiverUsername, message)
        else:
            newChat = users.addChat(usersChat)
            if newChat:
                submitted = newChat.submitMessage(senderUsername, receiverUsername, message)
        
        dataMessage['senderUsername'] = senderUsername
        dataMessage['receiverUsername'] = receiverUsername
        dataMessage['message'] = message
        print(dataMessage)
        emit('message submitted', dataMessage, broadcast=True)

@app.route('/fetchMessages', methods=['POST'])
def fetchMessages():
    senderUsername = session['username']
    receiverUsername = request.form['receiverUsername']
    # join_room(senderUsername)
    session['currentReceiverUsername'] = receiverUsername

    usersChat = [senderUsername, receiverUsername]
    chat = users.searchChatByUsernames(usersChat)
    serializedChat = {}
    if chat:
        serializedChat = chat.serialize()
    # print(session)
    print('chat: ', serializedChat)
    return jsonify(serializedChat)

@app.route('/searchUsername', methods=['POST'])
def searchCurrentUsername():
    return session['username']

@app.route('/searchCurrentReceiverUsername', methods=['POST'])
def searchCurrentUsernameReceiver():
    # print('currentUsername searched: ', session['currentUsernameReceiver'])
    return session['currentReceiverUsername']