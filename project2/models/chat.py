class User():
    def __init__(self, id, username):
        self.id = id
        self.username = username

class Message():
    def __init__(self, idSender, idReceiver, message):
        self.idSender = idSender
        self.idReceiver = idReceiver
        self.message = message
