from application import app, session, flat, socketio, emit, send, flash, render_template, request, redirect, url_for, join_room, leave_room
from models.chat import *

@app.route('/chat', methods=['GET', 'POST'])
def login():
    sessionKeys = session.keys()
    if 'activeUser' in sessionKeys and 'user' in sessionKeys and 'currentChatId' in sessionKeys:
        if session['activeUser']:
            return render_template('logged/chat.html', username=session['user'].getUsername())
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
        session['currentChatId'] = -1
        return render_template('logged/chat.html', username=session['user'].getUsername())

@socketio.on('fetch contacts')
def fetchContacts():
    username = session['user'].getUsername()
    contacts = session['user'].getContacts()
    data = {
        'username': username,
        'contacts': contacts
    }
    emit('contacts', data)

@socketio.on('fetch messages')
def fetchMessages(data):
    messageData = {}
    try:
        chatId = int(data['chatId'])
        currentChat = session['user'].searchChat(chatId)
        if currentChat:
            if session['currentChatId'] != -1:
                leave_room(session['currentChatId'])
            join_room(chatId)
            session['currentChatId'] = int(chatId)
            messageData['chat'] = currentChat.serialize()
    except:
        pass
    return messageData

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
                "senderUsername": senderUsername,
                'message': message,
                'username': session['user'].getUsername()
            }
            currentChat.submitMessage(senderUsername, message)
            emit('message submitted', dataMessage, room=chatId)

@socketio.on('search users')
def searchUser(data):
    print(data)
    MAX_NUMBER_SEARCH_USERS = 10
    users = []
    if 'searched' in data and data['searched']:
        users = flat.searchUsers(data['searched'], MAX_NUMBER_SEARCH_USERS, 0, [])
    return users

@socketio.on('search user data')
def searchUserData(data):
    print(data)
    username = data['username']
    userData = {}
    foundUser = None
    isContact = True

    foundUser = session['user'].searchContact(username)
    if not foundUser:
        isContact = False
        foundUser = flat.searchUserByUsername(username)
    
    if foundUser:
        userData = foundUser.serialize()
        userData['isContact'] = isContact

    print(userData)
    return userData

@app.route('/searchUsername', methods=['POST'])
def searchCurrentUsername():
    return session['user'].getUsername()