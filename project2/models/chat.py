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

    def addChat(self, usersUsernames):
        chatUsers = []
        createdChat = None

        if len(usersUsernames) >= 2:
            for username in usersUsernames:
                foundUser = self.searchUserByUsername(username)
                if foundUser:
                    chatUsers.append(foundUser)
            if len(chatUsers) >= 2:
                createdChat = Chat(len(self.__chats), chatUsers)
                self.__chats.append(createdChat)

        return createdChat

    # Delete (maybe)
    # def searchChatByUsernames(self, users):
    #     i = 0
    #     foundChat = None
    #     while i < len(self.__chats) and not foundChat:
    #         currentChat = self.__chats[i]
    #         if currentChat.sameUsers(users):
    #             foundChat = currentChat
    #         i += 1 
    #     return foundChat

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
        self.__username = username
        self.__setChats([])
        self.__setContacts([])
        # self.__chatsIds = []

    def __setChats(self, chats):
        self.__chats = chats

    def __setContacts(self, contacts):
        self.__contacts = contacts

    def getId(self):
        return self.__id
        
    def getUsername(self):
        return self.__username

    def getContacts(self):
        return self.__contacts

    def addChat(self, chat):
        self.__chats.append(chat)

    def addContact(self, contact):
        added = False
        if contact:
            self.__contacts.append(contact)
            added = True
        return added

    def serialize(self):
        return {
            'id': self.__id,
            'username': self.__username,
            'chatsIds': self.__chatsIds
        }

class Message():
    def __init__(self, senderUsername, message):
        self.__senderUsername = senderUsername
        # self.__receiverUsername = receiverUsername
        self.__message = message

    def getUsernameSender(self):
        return self.__senderUsername
    
    # def getUsernameReceiver(self):
    #     return self.__receiverUsername

    def getMessage(self):
        return self.__message

    def serialize(self):
        return {
            'senderUsername': self.__senderUsername,
            # 'receiverUsername': self.__receiverUsername,
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

    # Delete (maybe)
    # def sameUsers(self, users):
    #     i = 0
    #     j = 0
    #     counter = 0
    #     equals = True
    #     foundIndices = []

    #     while i < len(users) and equals:
    #         equals = False
    #         while j < len(self.__users) and not equals:
    #             if j not in foundIndices and users[i] == self.__users[j].getUsername():
    #                 counter += 1
    #                 equals = True
    #                 foundIndices.append(j)
    #             j += 1
    #         j = 0
    #         i += 1
    #     return counter == len(self.__users)

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