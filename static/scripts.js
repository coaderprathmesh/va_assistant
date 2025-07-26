//an array to store chat history.
    const chatLog = [];
    const chatHistoryDiv = document.getElementById("chat-history");
//the div element to print history in html format.
    const toggleBtn = document.getElementById("toggle-history");

    // Toggle visibility
    toggleBtn.addEventListener("click", () => {
      if (chatHistoryDiv.style.display === "none") {
        chatHistoryDiv.style.display = "block";
        toggleBtn.textContent = "Hide Chat History";
      } else {
        chatHistoryDiv.style.display = "none";
        toggleBtn.textContent = "Show Chat History";
      }
    });
//this function ensures the visibility should be changed based on user's button clicks. 
    function renderChat(log) {
      let html = '';
      log.forEach(pair => {
        html += `
          <h2>${pair.user}</h2>
          <p>${pair.bot}</p>
        `;
      });
      chatHistoryDiv.innerHTML = html;
    }
//this function uses for eache loop to ittereate and print chats in the div element by using div.innerHTML tag.


async function handleChatSubmit() {
  const audio = new Audio("/static/AI_replied.mp3");
  const userInput = document.getElementById("chat_text").value;
  document.getElementById("chat_text").value = "";
document.getElementById("user_query").textContent = `you asked: ${userInput}`
document.getElementById("chat").textContent = "Please wait, assistant is working on your query....";
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: userInput})
  });

  const data = await response.json();

  audio.play();

  document.getElementById("chat").textContent = `V A assistant said: ${data.reply}`;

  chatLog.push({ user: userInput, bot: data.reply });
  renderChat(chatLog);
}
document.getElementById("touchMe").onclick = handleChatSubmit;

document.getElementById("chat_text").addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleChatSubmit();
  }
});

//the chat log is passed the dict with user's input, and bot's reply and hence added to the render function to update div tag simalteniously