document.addEventListener("DOMContentLoaded", function () {
  const messageInput = document.getElementById("text");
  const sendButton = document.getElementById("send");
  const messageContainer = document.getElementById("messageFormeight");

  async function sendMessage(message) {
    messageInput.value = "";

    // Create user message HTML with timestamp
    const userHtml = `<div class="d-flex justify-content-end mb-4">
                              <div class="msg_cotainer_send">${message}
                                <span class="msg_time_send">${getTime()}</span>
                              </div>
                              <div class="img_cont_msg">
                                <img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg">
                              </div>
                            </div>`;

    messageContainer.innerHTML += userHtml;

    try {
      const response = await getResponse(message);

      const botHtml = `<div class="d-flex justify-content-start mb-4">
                              <div class="img_cont_msg">
                                <img src="https://www.prdistribution.com/spirit/uploads/pressreleases/2019/newsreleases/d83341deb75c4c4f6b113f27b1e42cd8-chatbot-florence-already-helps-thousands-of-patients-to-remember-their-medication.png" class="rounded-circle user_img_msg">
                              </div>
                              <div class="msg_cotainer">${response}
                                <span class="msg_time">${getTime()}</span>
                              </div>
                            </div>`;

      messageContainer.innerHTML += botHtml;
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  }

  function getTime() {
    const date = new Date();
    const hour = date.getHours();
    const minute = date.getMinutes().toString().padStart(2, "0"); // Add leading zero for single digits
    return `${hour}:${minute}`;
  }

  messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage(messageInput.value);
    }
  });

  sendButton.addEventListener("click", function (event) {
    event.preventDefault();
    sendMessage(messageInput.value);
  });

  async function getResponse(message) {
    const url = "/get";

    // Create a request object with message data in the body
    const request = new Request(url, {
      method: "POST",
      body: JSON.stringify({ msg: message }), // Send message as JSON
      headers: { "Content-Type": "application/json" }, // Set content type
    });

    try {
      // Fetch the response and handle success/failure
      const response = await fetch(request);
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      return await response.text(); // Parse text response
    } catch (error) {
      throw new Error(`Error fetching response: ${error.message}`);
    }
  }
});
