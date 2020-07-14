document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket (in order to begin the communication in real time between the client and the server)
    const socket = io.connect(
        location.protocol + '//' + document.domain + ':' + location.port
    );

    // When connected
    socket.on('connect', function () {
        socket.emit('fetch contacts');
        searchInSession('/searchUsername').then((username) => {
            if (username) {
                loadChatUser(username);
            }
        });

        // Configure Submit message button
        document.querySelector('#btn-submit-msg').onclick = () => {
            const message = document.querySelector('#input-message').value;
            searchInSession('/searchCurrentReceiverUsername').then(
                (currentReceiverUsername) => {
                    console.log('currentReceiver: ', currentReceiverUsername);
                    socket.emit('submit message', {
                        message,
                        currentReceiverUsername,
                    });
                }
            );
        };
    });

    socket.on('contacts', (data) => {
        sessionStorage.setItem('contacts', JSON.stringify(data.contacts));
        // sessionStorage.setItem("username", data.username);
        loadUsers();
    });

    socket.on('message submitted', (data) => {
        // Show message sent by another user or the user itself
        searchInSession('/searchUsername').then((username) => {
            searchInSession('/searchCurrentReceiverUsername').then(
                (currentReceiverUsername) => {
                    const receiver = data.receiverUsername;
                    const sender = data.senderUsername;
                    console.log('DATOS:');
                    console.log('receptor actual: ' + currentReceiverUsername);
                    console.log('receptor del mensaje: ' + receiver);
                    console.log('emisor: ' + sender);
                    console.log('usuario actual: ' + username);

                    // prettier-ignore
                    if (username == sender || (username == receiver && currentReceiverUsername == sender)) {
                        loadMessage(
                            data.senderUsername,
                            data.message,
                            data.senderUsername == username
                        );
                    }
                }
            );
        });
    });

    function searchInSession(route) {
        const req = new XMLHttpRequest();
        req.open('POST', route);
        const response = new Promise((resolve, reject) => {
            req.onload = () => {
                resolve(req.responseText);
            };
        });
        req.send(null);
        return response;
    }

    function loadUsers() {
        const divUsers = document.querySelector('#chat-div-users-inside');
        let divUser;
        let userTitle;

        divUsers.innerHTML = '';
        console.log(sessionStorage);
        JSON.parse(sessionStorage.getItem('users')).forEach((username) => {
            divUser = document.createElement('div');
            divUser.setAttribute('class', 'div-user');
            userTitle = document.createElement('p');
            userTitle.setAttribute('class', 'p-user-title');
            userTitle.innerHTML = username;
            divUser.appendChild(userTitle);
            divUser.addEventListener('click', () => loadChatUser(username));
            divUsers.appendChild(divUser);
        });
    }

    function loadMessage(username, message, isCurrentUser) {
        let classToAdd;
        let position;

        if (isCurrentUser) {
            document.querySelector('#input-message').value = '';
            classToAdd = 'justify-content-end';
            position = 'right';
        } else {
            classToAdd = 'justify-content-start';
            position = 'left';
        }

        const divMessages = document.querySelector('#chat-div-messages-inside');

        const divMessage = document.createElement('div');
        divMessage.setAttribute('class', 'd-flex div-message');
        divMessage.classList.add(classToAdd);

        const divText = document.createElement('div');
        divText.setAttribute('class', 'message-div-text rounded');

        const authorMessage = document.createElement('p');
        authorMessage.setAttribute('class', 'title-author-message');
        authorMessage.innerHTML = username;
        authorMessage.style.textAlign = position;

        const p = document.createElement('p');
        p.setAttribute('class', 'message-content-text');
        p.innerHTML = message;
        divText.appendChild(authorMessage);
        divText.appendChild(p);

        divMessage.appendChild(divText);
        divMessages.appendChild(divMessage);

        // Scroll to show the new message forcing the top to be scroll's height (it actually goes up to its limit since it can't scroll farther than the height)
        divMessages.scrollTo({
            top: divMessages.scrollHeight,
            behavior: 'smooth',
        });
    }

    function loadChatUser(receiverUsername) {
        resetChat();
        const response = searchMessagesWith(receiverUsername);
        response.then((data) => {
            if (data) {
                if (data.messages) {
                    searchInSession('/searchUsername').then((username) => {
                        data.messages.forEach((messageData) => {
                            loadMessage(
                                messageData.senderUsername,
                                messageData.message,
                                messageData.senderUsername == username
                            );
                        });
                    });
                }
            }
        });
        // prettier-ignore
        document.querySelector('#chat-title-with-who').textContent = receiverUsername;
    }

    function resetChat() {
        const divMessages = document.querySelector('#chat-div-messages-inside');
        divMessages.innerHTML = '';
    }

    function searchMessagesWith(receiverUsername) {
        const request = new XMLHttpRequest();
        request.open('POST', '/fetchMessages');

        let response = new Promise((resolve, reject) => {
            request.onload = () => {
                console.log('request.responseText: ', request.responseText);
                respText = request.responseText;
                if (respText) {
                    resolve(JSON.parse(respText));
                } else {
                    reject(null);
                }
            };
        });
        const dataToSend = new FormData();
        dataToSend.append('receiverUsername', receiverUsername);
        request.send(dataToSend);
        return response;
    }

    document
        .querySelector('#input-message')
        .addEventListener('keypress', (event) => {
            if (event.keyCode == 13) {
                document.querySelector('#btn-submit-msg').onclick();
            }
        });
});
