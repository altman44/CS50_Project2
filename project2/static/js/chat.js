document.addEventListener("DOMContentLoaded", () => {
  let currentUser;

  // Connect to websocket (in order to begin the communication in real time between the client and the server)
  const socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );

  // When connected
  socket.on("connect", () => {
    socket.emit("fetch users");

    // Configure Submit message button
    document.querySelector("#btn-submit-msg").onclick = () => {
      const message = document.querySelector("#input-message").value;
      currentUser = true;
      socket.emit("submit message", { message });
    };
  });

  socket.on("users", (data) => {
    sessionStorage.setItem("users", JSON.stringify(data.users));
    loadUsers();
  });

  socket.on("message submitted", (data) => {
    // Show message sent by another user or the user itself
    loadMessage(data.username, data.message, currentUser);
    currentUser = false;
  });

  function loadUsers() {
    const divUsers = document.querySelector("#chat-div-users-inside");
    let divUser;
    let userTitle;

    divUsers.innerHTML = "";
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

  function loadChatUser(idReceiver) {
    resetChat();
    const response = searchMessagesWith(idReceiver);
    response.then(data => {
      data.messages.forEach(messageData => {
        loadMessage(
          messageData.idSender,
          messageData.message,
          messageData.idReceiver == idReceiver
        );
      });
    })
    
    document.querySelector("#chat-title-with-who").textContent = idReceiver;
  }

  function resetChat() {
    const divMessages = document.querySelector("#chat-div-messages-inside");
    divMessages.innerHTML = "";
  }

  function searchMessagesWith(idReceiver) {

    const request = new XMLHttpRequest();
    request.open("POST", "/fetchMessages");

    let response = new Promise((resolve, reject) => {
      request.onload = () => {
        try {
          resolve(JSON.parse(request.responseText));
        } catch (e) {
          reject(e)
        }
      }
    });

    const dataToSend = new FormData();
    dataToSend.append("idReceiver", idReceiver);
    request.send(dataToSend);
    return response;
  }

  document
    .querySelector("#input-message")
    .addEventListener("keypress", (event) => {
      if (event.keyCode == 13) {
        document.querySelector("#btn-submit-msg").onclick();
      }
    });
});
