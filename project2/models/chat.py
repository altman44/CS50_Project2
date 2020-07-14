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
            # for user in users:
                # foundUser = self.searchUserByUsername(username)
                # chatUsers.append(foundUser)
            # if len(chatUsers) >= 2:
            createdChat = Chat(len(self.__chats), users)
            self.__chats.append(createdChat)
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
                'username': contact.getUsername(),
                'chatId': self.searchChatIdWith(contact)
            }
            contacts.append(newContactData)
        return contacts

    def searchChatIdWith(self, contact):
        i = 0
        foundContact = None
        chatId = -1

        while i < len(self.__chats) and not foundContact:
            currentChat = self.__chats[i]
            if currentChat.search
        return chatId

    def addChat(self, chat):
        self.__chats.append(chat)

    def addContact(self, contactId, chatId):
        added = False
        if contactId is not None and chatId is not None:
            newContact = Contact(contactId, chatId)
            self.__contacts.append(newContact)
            added = True
        return added

    def searchChat(self, chatId):
        i = 0
        foundChat = None

        while i < len(self.__chats) and not foundChat:
            currentChat = self.__chats[i]
            if (currentChat.getId() == chatId):
                foundChat = currentChat
            i += 1
        return foundChat

    def serialize(self):
        return {
            'id': self.__id,
            'username': self.__username,
            'chatsIds': self.__chatsIds
        }

class Contact():
    def __init__(self, id, chatId):
        self.__id = id
        self.__chatId = chatId
    
    def getId(self):
        return self.__id
    
    def getChatId(self):
        return self.__chatId

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
        self.setUsers(users)
        self.setMessages([])
    
    def setUsers(self, users):
        ok = False
        if len(users) >= 2:
            self.__users = users
            ok = True
        return ok
    
    def setMessages(self, messages):
        self.__messages = messages

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
            'users': serializedUsers,
            'messages': serializedMessages
        }