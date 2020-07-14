class Flat():
    def __init__(self):
        self.__users = []
        self.__chats = []

    def getUsersUsernames(self):
        newArrWithUsernames = []
        for user in self.__users:
            newArrWithUsernames.append(user.getUsername())
        return newArrWithUsernames

    def addUser(self, username):
        createdUser = None
        foundUser = self.searchUserByUsername(username)
        if not foundUser:
            createdUser = User(len(self.__users), username)
            self.__users.append(createdUser)
        return createdUser

    def deleteUser(self, username):
        deletedUser = None
        foundUser = self.searchUser(username)
        if foundUser:
            self.__users.remove(foundUser)
            deletedUser = foundUser
        return deletedUser

    def searchUserByUsername(self, username):
        i = 0
        foundUser = None
        while i < len(self.__users) and not foundUser:
            currentUser = self.__users[i]
            if currentUser.getUsername() == username:
                foundUser = currentUser
            i += 1
        return foundUser

    def addChat(self, users):
        chatUsers = []
        createdChat = None

        if len(users) >= 1:
            createdChat = Chat(len(self.__chats), users)
            self.__chats.append(createdChat)
            for user in users:
                user.addChat(createdChat)
        return createdChat

    def serialize(self):
        serializedUsers = []
        serializedChats = []

        for user in self.__users:
            serializedUsers.append(user.serialize())

        for chat in self.__chats:
            serializedChats.append(chat.serialize())
        
        return {
            'users': serializedUsers,
            'cantUsers': self.__cantUsers,
            'chats': serializedChats
        }

class User():
    def __init__(self, id, username):
        self.__id = id
        self.__setUsername(username)
        self.__setChats([])
        self.__setContacts([])

    def __setUsername(self, username):
        if username:
            self.__username = username            

    def __setChats(self, chats):
        self.__chats = chats

    def __setContacts(self, contacts):
        self.__contacts = contacts

    def getId(self):
        return self.__id
        
    def getUsername(self):
        return self.__username

    def getChats(self):
        return self.__chats

    def getContacts(self):
        return self.__contacts

    def getContacts(self):
        contacts = []
        for contact in self.__contacts:
            newContactData = {
                'username': contact.getUser().getUsername(),
                'chatId': contact.getChat().getId()
            }
            contacts.append(newContactData)
        return contacts

    def addChat(self, chat):
        self.__chats.append(chat)

    def searchChat(self, chatId):
        i = 0
        foundChat = None

        try:
            chatId = int(chatId)
            while i < len(self.__chats) and not foundChat:
                currentChat = self.__chats[i]
                if currentChat.getId() == chatId:
                    foundChat = currentChat
                i += 1
        except TypeError:
            pass
        finally:
            return foundChat

    def addContact(self, user, chat):
        newContact = None
        if user and chat:
            newContact = Contact(user, chat)
            self.__contacts.append(newContact)
        return newContact

    def searchContact(self, username):
        i = 0
        foundContact = None

        while i < len(self.__contacts) and not foundContact:
            currentContact = self.__contacts[i]
            if currentContact.getUsername() == username:
                foundContact = currentContact
            i += 1
        return foundContact

    def serialize(self):
        return {
            'id': self.__id,
            'username': self.__username
        }

class Contact():
    def __init__(self, user, chat):
        self.__setUser(user)
        self.__chat = chat
    
    def __setUser(self, user):
        if user:
            self.__user = user

    def __setChatId(self, chat):
        if chat:
            self.__chat = chat

    def getUser(self):
        return self.__user
    
    def getChat(self):
        return self.__chat

    def serialize(self):
        return {
            'user': self.__user.serialize(),
            'chat': self.__chat.serialize()
        }

class Message():
    def __init__(self, senderUsername, message):
        self.__senderUsername = senderUsername
        self.__message = message

    def getUsernameSender(self):
        return self.__senderUsername

    def getMessage(self):
        return self.__message

    def serialize(self):
        return {
            'senderUsername': self.__senderUsername,
            'message': self.__message
        }

class Chat():
    def __init__(self, id, users):
        self.__id = id
        print('users: ', users)
        self.setUsers(users)
        self.setMessages([])
    
    def setUsers(self, users):
        ok = False
        if len(users) >= 1:
            self.__users = users
            ok = True
        return ok
    
    def setMessages(self, messages):
        self.__messages = messages

    def getId(self):
        return self.__id

    def submitMessage(self, senderUsername, message):
        createdMsg = None
        if senderUsername and message:
            createdMsg = Message(senderUsername, message)
            self.__messages.append(createdMsg)
        return createdMsg

    def serialize(self):
        serializedMessages = []
        serializedUsers = []

        for msg in self.__messages:
            serializedMessages.append(msg.serialize())

        for user in self.__users:
            serializedUsers.append(user.serialize())

        return {
            'id': self.__id,
            'messages': serializedMessages
        }