from application import app, session, flat, socketio, emit, send, flash, render_template, request, redirect, url_for, join_room, leave_room
from models.chat import *
from helpers.chatId_enum import ChatId

@app.route('/chat', methods=['GET', 'POST'])
def login():
    # sessionKeys = session.keys()
    # if 'activeUser' in sessionKeys and 'username' in sessionKeys and 'currentChatId' in sessionKeys:
    if 'username' in session and 'currentChatId' in session:
        if session['username']:
            return render_template('logged/chat.html', username=session['username'])
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
        if flat.searchUserByUsername(username):
            flash('The username already exists', 'danger')
            return redirect(url_for('index'))

        user = flat.searchUserByUsername(username)
        if not user:
            user = flat.addUser(username)

        createdChat = flat.addChat([user])
        user.addContact(user, createdChat)
        createdChat.submitMessage(username, "By this chat, you can send messages to yourself")

        session['username'] = username
        # session['activeUser'] = True
        session['currentChatId'] = -1
        return render_template('logged/chat.html', username=username)

@socketio.on('fetch contacts')
def fetchContacts():
    username = session['username']
    user = searchUser(None, username)[0]
    print(user)
    if user:
        contacts = user.getContacts()
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
        user = searchUser(None, session['username'])[0]
        if user:
            currentChat = user.searchChat(chatId)
            if currentChat:
                if session['currentChatId'] >= ChatId.OK_MIN:
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
    
    if chatId >= ChatId.OK_MIN:
        if message:
            user = searchUser(None, session['username'])[0]
            # currentChat = session['user'].searchChat(chatId)
            if user:
                currentChat = user.searchChat(chatId)
                if currentChat:
                    senderUsername = session['username']
                    # senderUsername = session['user'].getUsername()
                    dataMessage = {
                        'senderUsername': senderUsername,
                        'message': message
                    }
                    currentChat.submitMessage(senderUsername, message)
                    emit('message submitted', dataMessage, room=chatId)
    # elif chatId == ChatId.WAITING:
    #     if message:
    #         currentChatUser = session['currentChatUser']
    #         if currentChatUser:
    #             users = [session['user'], currentChatUser]
    #             createdChat = flat.addChat(users)
    #             for user in users:
    #                 user.addChat(createdChat)
    #             chatId = createdChat.getId()
    #             username = session['user'].getUsername()
    #             dataMessage = {
    #                 'senderUsername': username,
    #                 'message': message
    #             }
    #             createdChat.submitMessage(username, message)
    #             join_room(chatId)
    #             session['currentChatUser'] = None
    #             session['currentChatId'] = chatId
    #             emit('message submitted', dataMessage, room=chatId)

@socketio.on('search users')
def searchUser(data):
    MAX_NUMBER_SEARCH_USERS = 10
    users = []
    if 'searched' in data and data['searched']:
        users = flat.searchUsers(data['searched'], MAX_NUMBER_SEARCH_USERS, 0, [])
    return users

@socketio.on('search user data')
def searchUserData(data):
    username = data['username']
    userData = {}
    foundUser = None
    if username:
        user = searchUser(None, session['username'])[0]
        if user:
            searched = searchUser(user, username)
            foundUser = searched[0]
            isContact = searched[1]

            if foundUser:
                serializedUser = foundUser.serialize()
                if isContact:
                    userData = serializedUser
                else:
                    userData['user'] = serializedUser
                    chat = user.searchChatWith(foundUser)
                    if chat:
                        userData['chat'] = chat.serialize()

            userData['isContact'] = isContact
            # userData['chatId'] = session['currentChatId']
            # userData['enumChatId'] = ChatId
    return userData

@socketio.on('create chat')
def createChat(data):
    username = data['username']
    if username:
        user = searchUser(None, session['username'])[0]
        if user:
            foundUser = searchUser(user, username)[0]
            if foundUser:
                users = [user, foundUser]
                foundChat = user.searchChatWith(foundUser)
                if foundChat:
                    chatId = foundChat.getId()
                else:
                    createdChat = flat.addChat(users)
                    chatId = createdChat.getId()

                if data['joinChat']:
                    if session['currentChatId'] >= ChatId.OK_MIN:
                        leave_room(session['currentChatId'])
                    join_room(chatId)
                    session['currentChatId'] = chatId
                # session['currentChatUser'] = foundUser
                # session['currentChatId'] = ChatId.WAITING

# @app.route('/searchUsername', methods=['POST'])
# def searchCurrentUsername():
#     return session['user'].getUsername()

def searchUser(userInstance, username):
    """Search in contacts first, if it isn't there, throughout the application."""
    isContact = True
    foundUser = None
    if userInstance:
        foundUser = userInstance.searchContact(username)
    if not foundUser:
        isContact = False
        foundUser = flat.searchUserByUsername(username)
    return (foundUser, isContact)
