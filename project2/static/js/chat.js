document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket (in order to begin the communication in real time between the client and the server)
    const socket = io.connect(
        location.protocol + '//' + document.domain + ':' + location.port
    );

    // When connected
    socket.on('connect', () => {
        socket.emit('fetch contacts');

        // Configure Submit message button
        document.querySelector('#btn-submit-msg').onclick = () => {
            const message = document.querySelector('#input-message').value;
            if (message) {
                socket.emit('submit message', { message });
            }
        };
    });

    socket.on('disconnect', () => {
        console.log('DISCONNECTION, you cannot send messages!');
    });

    socket.on('contacts', data => {
        sessionStorage.setItem('username', data.username);
        sessionStorage.setItem('contacts', JSON.stringify(data.contacts));
        loadUsers();
    });

    socket.on('message submitted', data => {
        // Show message sent by another user or the user itself
        const sender = data.senderUsername;
        // prettier-ignore
        loadMessage(
            data.senderUsername,
            data.message,
            data.senderUsername === sessionStorage.getItem('username')
        );
    });

    function loadUsers() {
        const divUsers = document.querySelector('#chat-div-users-inside');
        let divUser;
        let userTitle;

        divUsers.innerHTML = '';
        console.log(sessionStorage);
        const contacts = JSON.parse(sessionStorage.getItem('contacts'));
        contacts.forEach(contact => {
            console.log(contact);
            divUser = document.createElement('div');
            divUser.setAttribute('class', 'div-user');
            userTitle = document.createElement('p');
            userTitle.setAttribute('class', 'p-user-title');
            userTitle.innerHTML = contact.username;
            divUser.appendChild(userTitle);
            divUser.addEventListener('click', () =>
                loadChatUser(contact.chatId)
            );
            divUsers.appendChild(divUser);
        });
    }

    function loadMessage(username, message, isCurrentUser) {
        let classToAdd;
        let position;
        const divMessages = document.querySelector('#chat-div-messages-inside');
        const scrollHeight = divMessages.scrollHeight;
        const clientHeight = divMessages.clientHeight;
        const scrollTop = divMessages.scrollTop;

        if (isCurrentUser) {
            document.querySelector('#input-message').value = '';
            classToAdd = 'justify-content-end';
            position = 'right';
        } else {
            classToAdd = 'justify-content-start';
            position = 'left';
        }

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
        // If the user is not at the bottom of the chat, it will not scroll
        // prettier-ignore
        if (scrollTop === (scrollHeight - clientHeight) || scrollHeight === clientHeight) {
            divMessages.scrollTo({
                top: scrollHeight,
                behavior: 'smooth'
            });
        }
    }

    function loadChatUser(chatId) {
        resetChat();
        const divMessages = document.querySelector('#chat-div-messages-inside');

        if (divMessages.style.overflowY === '') {
            console.log('entro');
            divMessages.style.overflowY = 'scroll';
            divMessages.style.overFlowX = 'hidden';
            divMessages.scrollBehavior = 'smooth';
        }

        socket.emit('fetch messages', { chatId }, data => {
            if (data) {
                const username = sessionStorage.getItem('username');
                // prettier-ignore
                document.querySelector('#chat-title-with-who').textContent = username;
                if (data.chat) {
                    const messages = data.chat.messages;
                    if (messages) {
                        messages.forEach(messageData => {
                            loadMessage(
                                messageData.senderUsername,
                                messageData.message,
                                messageData.senderUsername === username
                            );
                        });
                    }
                    // prettier-ignore
                    document.querySelector('#chat-div-submit').style.visibility = 'visible';
                    document.querySelector('#input-message').focus();
                }
            }
        });
    }

    function resetChat() {
        const divMessages = document.querySelector('#chat-div-messages-inside');
        divMessages.innerHTML = '';
    }

    // prettier-ignore
    document.querySelector('#input-message').addEventListener('keypress', (event) => {
        if (event.keyCode === 13) {
            document.querySelector('#btn-submit-msg').onclick();
        }
    });

    // prettier-ignore
    document.querySelector('#input-search-users')
        .addEventListener('input', function(event) {
            const searchedUsername = this.value;
            if (!event.inputType) {
                // it means a datalist option was selected
                showUserData(searchedUsername);
            } else {
                searchUsers(searchedUsername)
                .then(usernames => {
                    const dataList = document.querySelector('#list-users');
                    appendOptionsToDataList(dataList, usernames);
                })
            }
        });

    function searchUsers(searched) {
        return new Promise((resolve, reject) => {
            socket.emit('search user', { searched }, usernames => {
                resolve(usernames);
            });
        });
    }

    function appendOptionsToDataList(dataList, array) {
        dataList.innerHTML = '';
        array.forEach(element => {
            let newOption = document.createElement('option');
            newOption.addEventListener('onclick', () => {
                console.log('hey');
            });
            newOption.value = element;
            dataList.appendChild(newOption);
        });
    }

    function showUserData(username) {

    }
});
