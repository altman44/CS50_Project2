class Flat():
    def __init__(self):
        self.__users = []
        self.__chats = []

    def searchUsers(self, search, maxSearchUsers, counter, foundUsers):
        if counter < maxSearchUsers and counter < len(self.__users) and counter >= 0:
            foundUsers = foundUsers
            user = self.__users[counter]
            username = user.getUsername()
            if search in username:
                foundUsers.append(username)
            counter += 1
            return self.searchUsers(search, maxSearchUsers, counter, foundUsers)
        return foundUsers

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
        if chat:
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

    def searchChatWith(self, user):
        chat = None
        if user:
            i = 0
            users = [self, user]
            while i < len(self.__chats) and not chat:
                currentChat = self.__chats[i]
                if currentChat.sameUsers(users):
                    chat = currentChat
                i += 1
        return chat

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

    def getUsername(self):
        return self.__user.getUsername()
    
    def getChat(self):
        return self.__chat

    def serialize(self):
        return {
            'user': self.__user.serialize(),
            'chat': self.__chat.serialize()
        }

class Message():
    def __init__(self, senderUsername, message):
        self.__setSenderUsername(senderUsername)
        self.__setMessage(message)

    def __setSenderUsername(self, username):
        if username:
            self.__senderUsername = username        

    def __setMessage(self, message):
        if message:
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
        if len(users) >= 1:
            self.__users = users
            ok = True
        return ok
    
    def setMessages(self, messages):
        self.__messages = messages

    def getId(self):
        return self.__id

    def sameUsers(self, users):
        j = 0
        k = 0
        counter = 0
        repeated = True
        if len(users) == len(self.__users):
            addedUsers = []
            while j < len(self.__users) and repeated:
                repeated = False
                currentUser = self.__users[j]
                k = 0
                while k < len(users) and not repeated:
                    if currentUser not in addedUsers and currentUser.getUsername() == users[k].getUsername():
                        counter += 1
                        repeated = True
                        addedUsers.append(currentUser)
                    k += 1
                j += 1
            return counter == len(self.__users)
        return False

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