document.addEventListener("DOMContentLoaded", () => {

  // Connect to websocket (in order to begin the communication in real time between the client and the server)
  const socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );

  // When connected
  socket.on("connect", function () {
    socket.emit("fetch users");

    //const username = sessionStorage.getItem("username");
    const getUsername = searchCurrentUsername();
    getUsername.then(username => {
      if (username) {
        loadChatUser(username);
      }
    });

    // Configure Submit message button
    document.querySelector("#btn-submit-msg").onclick = (usernameReceiver) => {
      const message = document.querySelector("#input-message").value;
      //let usernameReceiver = sessionStorage.getItem("usernameReceiver");
      socket.emit("submit message", { message, usernameReceiver });
    };
  });

  socket.on("users", (data) => {
    sessionStorage.setItem("users", JSON.stringify(data.users));
    // sessionStorage.setItem("username", data.username);
    loadUsers();
  });

  socket.on("message submitted", (data) => {
    // Show message sent by another user or the user itself
    const getUsername = searchCurrentUsername();
    getUsername.then(username => {
      console.log('username: ', username);
      loadMessage(data.usernameSender, data.message, data.usernameSender == username);    
    })
  });

  function searchCurrentUsername() {
    const req = new XMLHttpRequest();
    req.open('POST', '/searchCurrentUsername');
    const response = new Promise((resolve, reject) => {
      req.onload = () => {
        console.log(req.responseText);
        resolve('Hi');
      }
    })
    return response
  }

  function loadUsers() {
    const divUsers = document.querySelector("#chat-div-users-inside");
    let divUser;
    let userTitle;

    divUsers.innerHTML = "";
    console.log(sessionStorage)
    JSON.parse(sessionStorage.getItem("users")).forEach(username => {
      divUser = document.createElement("div");
      divUser.setAttribute("class", "div-user");
      userTitle = document.createElement("p");
      userTitle.setAttribute("class", "p-user-title");
      userTitle.innerHTML = username;
      divUser.appendChild(userTitle);
      divUser.addEventListener("click", () => loadChatUser(username));
      divUsers.appendChild(divUser);
    });
  }

  function loadMessage(username, message, isCurrentUser) {
    let classToAdd;
    let position;

    if (isCurrentUser) {
      document.querySelector("#input-message").value = "";
      classToAdd = "justify-content-end";
      position = "right";
    } else {
      classToAdd = "justify-content-start";
      position = "left";
    }

    const divMessages = document.querySelector("#chat-div-messages-inside");

    const divMessage = document.createElement("div");
    divMessage.setAttribute("class", "d-flex div-message");
    divMessage.classList.add(classToAdd);

    const divText = document.createElement("div");
    divText.setAttribute("class", "message-div-text rounded");

    const authorMessage = document.createElement("p");
    authorMessage.setAttribute("class", "title-author-message");
    authorMessage.innerHTML = username;
    authorMessage.style.textAlign = position;

    const p = document.createElement("p");
    p.setAttribute("class", "message-content-text");
    p.innerHTML = message;
    divText.appendChild(authorMessage);
    divText.appendChild(p);

    divMessage.appendChild(divText);
    divMessages.appendChild(divMessage);

    // Scroll to show the new message forcing the top to be scroll's height (it actually goes up to its limit since it can't scroll farther than the height)
    divMessages.scrollTo({
      top: divMessages.scrollHeight,
      behavior: "smooth",
    });
  }

  function loadChatUser(usernameReceiver) {
    resetChat();
    const response = searchMessagesWith(usernameReceiver);
    response.then((data) => {
      if (data) {
        if (data.messages) {
          data.messages.forEach((messageData) => {
            loadMessage(
              messageData.usernameSender,
              messageData.message,
              messageData.usernameSender == sessionStorage.getItem('username')
            );
          });
        }
      }
    });

    document.querySelector(
      "#chat-title-with-who"
    ).textContent = usernameReceiver;
  }

  function resetChat() {
    const divMessages = document.querySelector("#chat-div-messages-inside");
    divMessages.innerHTML = "";
  }

  function searchMessagesWith(usernameReceiver) {
    const request = new XMLHttpRequest();
    request.open("POST", "/fetchMessages");

    let response = new Promise((resolve, reject) => {
      request.onload = () => {
        try {
          console.log("request.responseText: ", request.responseText);
          respText = request.responseText;
          if (respText) {
            resolve(JSON.parse(respText));
          } else {
            reject(null);
          }
        } catch (e) {
          reject(e);
        }
      };
    });

    const dataToSend = new FormData();
    dataToSend.append("usernameReceiver", usernameReceiver);
    request.send(dataToSend);
    return response;
  }

  document
    .querySelector("#input-message")
    .addEventListener("keypress", (event) => {
      if (event.keyCode == 13) {
        document.querySelector("#btn-submit-msg").onclick(sessionStorage.getItem('username'));
      }
    });
});
