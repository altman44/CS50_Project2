from application import app, session, flat, socketio, emit, flash, render_template, request, redirect, url_for, join_room
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
        user.addChat(createdChat)
        createdChat.submitMessage(username, "Por este chat podés enviarte mensajes a vos mismo")

        session['user'] = user
        user.addContact(user)
        session['activeUser'] = True
        session['currentReceiverUsername'] = ""
        return render_template('logged/chat.html')

@socketio.on('fetch contacts')
def fetchUsers():
    data = {}
    data['username'] = session['user'].getUsername()
    # data['users'] = flat.getUsersUsernames()
    data['contacts'] = session['user'].getContacts()
    emit('contacts', data, broadcast=True)

@app.route('/fetchMessages', methods=['POST'])
def fetchMessages():
    chatId = request.form['chatId']
    print("chatId: ", chatId)
    currentChat = session['user'].searchChat(chatId)
    if currentChat:
        join_room(chatId)
        session['currentChatId'] = chatId
        data = {
            'username': session['user'].getUsername(),
            'chat': currentChat.serialize()
        }
        print('chat: ', data)
        return jsonify(data)
    return {}

@socketio.on('submit message')
def message(data):
    chatId = session['currentChatId']
    message = data['message']

    if message:
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

# @app.route('/searchCurrentReceiverUsername', methods=['POST'])
# def searchCurrentUsernameReceiver():
#     # print('currentUsername searched: ', session['currentUsernameReceiver'])
#     return session['currentReceiverUsername']