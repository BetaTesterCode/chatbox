// Function to send message to the backend
function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const message = userInput.value;

    if (message.trim() === '') return; // Don't send empty messages

    // Display user message in the chat box
    const userMessageContainer = document.createElement('div');
    userMessageContainer.classList.add('message-container', 'user');

    const userAvatarDiv = document.createElement('div');
    userAvatarDiv.classList.add('avatar');
    // Set background image for user avatar (replace with actual image URL)
    userAvatarDiv.style.backgroundImage = 'url("https://via.placeholder.com/35/0f4c75/ffffff?text=You")'; // Placeholder image

    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message');
    userMessageDiv.textContent = message; // Display only the message text

    // Add the user-message class to the message content div
    userMessageDiv.classList.add('user-message');

    userMessageContainer.appendChild(userMessageDiv);
    userMessageContainer.appendChild(userAvatarDiv);
    chatBox.appendChild(userMessageContainer);

    // Send message to Flask backend
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.response;
        
        // Display bot response in the chat box
        const botMessageContainer = document.createElement('div');
        botMessageContainer.classList.add('message-container', 'bot');

        const botAvatarDiv = document.createElement('div');
        botAvatarDiv.classList.add('avatar');
        // Set background image for bot avatar (replace with actual image URL)
        botAvatarDiv.style.backgroundImage = 'url("https://via.placeholder.com/35/3282b8/ffffff?text=Bot")'; // Placeholder image

        const botMessageDiv = document.createElement('div');
        botMessageDiv.classList.add('message');
        // Add the bot-message class to the message content div
        botMessageDiv.classList.add('bot-message');
        // Use innerHTML and convertMarkdownToHtml
        botMessageDiv.innerHTML = convertMarkdownToHtml(botResponse);

        botMessageContainer.appendChild(botAvatarDiv);
        botMessageContainer.appendChild(botMessageDiv);
        chatBox.appendChild(botMessageContainer);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error sending message:', error);
        const errorMessageDiv = document.createElement('div');
        errorMessageDiv.classList.add('message', 'bot-message');
        errorMessageDiv.style.color = 'red';
        errorMessageDiv.textContent = 'Bot: Sorry, there was an error.';
        chatBox.appendChild(errorMessageDiv);
         chatBox.scrollTop = chatBox.scrollHeight;
    });

    // Clear the input field
    userInput.value = '';
}

// Optional: Send message on pressing Enter key
document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Function to convert basic Markdown to HTML
function convertMarkdownToHtml(text) {
    // Convert **bold** to <strong>bold</strong>
    let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Convert newline to <br>
    html = html.replace(/\n/g, '<br>');
    return html;
} 