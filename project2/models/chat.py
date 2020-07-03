class Users():
    def __init__(self):
        self.__users = []
        self.__cantUsers = 0
        self.__chats = []

    def __getChatsLength(self):
        return len(self.__chats)

    def getUsersUsernames(self):
        newArrWithUsernames = []
        for user in self.__users:
            newArrWithUsernames.append(user.getUsername())
        return newArrWithUsernames

    def appendUser(self, username):
        added = False
        userFound = self.searchUserByUsername(username)
        if not userFound:
            userCreated = User(self.__cantUsers, username)
            self.__cantUsers += 1
            self.__users.append(userCreated)
            added = True
        return added

    def deleteUser(self, username):
        deleted = False
        userFound = self.searchUser(username)
        if userFound:
            self.__users.remove(userFound)
            self.__cantUsers -= 1
            deleted = True
        return deleted

    # def searchUserById(self, id):
    #     i = 0
    #     userFound = None
    #     while i < (self.__users) and not userFound:
    #         currentUser = self.__users[i]
    #         if currentUser.getId() == id:
    #             userFound = currentUser
    #         i += 1
    #     return userFound

    def searchUserByUsername(self, username):
        i = 0
        userFound = None
        while i < len(self.__users) and not userFound:
            currentUser = self.__users[i]
            if currentUser.getUsername() == username:
                userFound = currentUser
            i += 1
        return userFound

    def appendChat(self, usersUsername):
        chatUsers = []
        chatCreated = None

        if len(usersUsername) >= 2:
            for username in usersUsername:
                userFound = self.searchUserByUsername(username)
                if userFound:
                    chatUsers.append(userFound)
            if len(chatUsers) >= 2:
                chatCreated = Chat(self.__getChatsLength(), chatUsers)
                self.__chats.append(chatCreated)

        return chatCreated

    def searchChatByUsernames(self, users):
        i = 0
        chatFound = None
        while i < len(self.__chats) and not chatFound:
            currentChat = self.__chats[i]
            if currentChat.sameUsers(users):
                chatFound = currentChat
            i += 1 
        return chatFound

    def serialize(self):
        usersSerialized = []
        chatsSerialized = []

        for user in self.__users:
            usersSerialized.append(user.serialize())

        for chat in self.__chats:
            chatsSerialized.append(chat.serialize())
        
        return {
            'users': usersSerialized,
            'cantUsers': self.__cantUsers,
            'chats': chatsSerialized
        }

class User():
    def __init__(self, id, username):
        self.__id = id
        self.__username = username
        self.__chatsIds = []
        # self.__messages = []

    # def submitMessage(self, usernameReceiver, message):
    #     msg = Message(self.__username, usernameReceiver, message)
    #     self.__messages.append(msg.__dict__)

    def getId(self):
        return self.__id
        
    def getUsername(self):
        return self.__username

    def appendChat(self, idChat):
        self.__chatsIds.append(idChat)

    def serialize(self):
        return {
            'id': self.__id,
            'username': self.__username,
            'chatsIds': self.__chatsIds
        }

    # def getMessages(self):
    #     newArrWithMsgs = []
    #     for msg in self.__messages:
    #         newArrWithMsgs.append(msg.__dict__)
    #     return newArrWithMsgs

class Message():
    def __init__(self, usernameSender, usernameReceiver, message):
        self.__usernameSender = usernameSender
        self.__usernameReceiver = usernameReceiver
        self.__message = message

    def getUsernameSender(self):
        return self.__usernameSender
    
    def getUsernameReceiver(self):
        return self.__usernameReceiver

    def getMessage(self):
        return self.__message

    def serialize(self):
        return {
            'usernameSender': self.__usernameSender,
            'usernameReceiver': self.__usernameReceiver,
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

    def submitMessage(self, usernameSender, usernameReceiver, message):
        submitted = False
        if usernameSender and usernameReceiver and message:
            msg = Message(usernameSender, usernameReceiver, message)
            self.__messages.append(msg)
            submitted = True
        return submitted

    def sameUsers(self, users):
        i = 0
        j = 0
        counter = 0
        equals = True
        indexesFound = []

        while i < len(users) and equals:
            equals = False
            while j < len(self.__users) and not equals:
                if j not in indexesFound and users[i] == self.__users[j].getUsername():
                    counter += 1
                    equals = True
                    indexesFound.append(j)
                j += 1
            j = 0
            i += 1
        return counter == len(self.__users)

    def serialize(self):
        messagesSerialized = []
        usersSerialized = []

        for msg in self.__messages:
            messagesSerialized.append(msg.serialize())

        for user in self.__users:
            usersSerialized.append(user.serialize())

        return {
            'id': self.__id,
            'users': usersSerialized,
            'messages': messagesSerialized
        }