from application import app, session, flat, socketio, emit, send, flash, render_template, request, redirect, url_for, join_room, leave_room
from flask import jsonify
from models.chat import *

@app.route('/chat', methods=['GET', 'POST'])
def login():
    sessionKeys = session.keys()
    if 'activeUser' in sessionKeys and 'user' in sessionKeys and 'currentChatId' in sessionKeys:
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

        user = flat.searchUserByUsername(username)
        if not user:
            user = flat.addUser(username)

        createdChat = flat.addChat([user])
        user.addContact(user, createdChat)
        createdChat.submitMessage(username, "Por este chat podés enviarte mensajes a vos mismo")

        session['user'] = user
        session['activeUser'] = True
        session['currentChatId'] = None
        return render_template('logged/chat.html')

@socketio.on('fetch contacts')
def fetchContacts():
    data = {}
    data['username'] = session['user'].getUsername()
    data['contacts'] = session['user'].getContacts()
    emit('contacts', data)

@socketio.on('fetch messages')
def fetchMessages(data):
    data = {}
    try:
        chatId = int(data['chatId'])
        currentChat = session['user'].searchChat(chatId)
        if currentChat:
            if session['currentChatId'] != -1:
                leave_room(session['currentChatId'])
            join_room(chatId)
            session['currentChatId'] = int(chatId)
            data['username'] = session['user'].getUsername()
            data['chat'] = currentChat.serialize()
    return data

@socketio.on('submit message')
def message(data):
    chatId = session['currentChatId']
    message = data['message']
    print('chatId: ', chatId)
    if message and chatId != -1:
        currentChat = session['user'].searchChat(chatId)
        if currentChat:
            senderUsername = session['user'].getUsername()
            dataMessage = {
                "sender": senderUsername,
                'message': message,
                'username': session['user'].getUsername()
            }
            currentChat.submitMessage(senderUsername, message)
            emit('message submitted', dataMessage, room=chatId)

    # if message and receiverUsername:
    #     submitted = False
    #     dataMessage = {}

    #     senderUsername = session['username']
    #     usersChat = [senderUsername, receiverUsername]
    #     print(f"sender: {senderUsername} y receiver: {receiverUsername}")
    #     chatFound = flat.searchChatByUsernames(usersChat)

    #     if chatFound:
    #         submitted = chatFound.submitMessage(senderUsername, receiverUsername, message)
    #     else:
    #         newChat = flat.addChat(usersChat)
    #         if newChat:
    #             submitted = newChat.submitMessage(senderUsername, receiverUsername, message)
        
    #     dataMessage['senderUsername'] = senderUsername
    #     dataMessage['receiverUsername'] = receiverUsername
    #     dataMessage['message'] = message
    #     print(dataMessage)
    #     emit('message submitted', dataMessage, broadcast=True)

@app.route('/searchUsername', methods=['POST'])
def searchCurrentUsername():
    return session['user'].getUsername()