document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatClose = document.getElementById('chat-close');
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    console.log("Chat script loaded");

    // Toggle Chat Window
    function toggleChat() {
        chatWindow.classList.toggle('hidden');
        if (!chatWindow.classList.contains('hidden')) {
            chatInput.focus();
        }
    }

    chatToggle.addEventListener('click', toggleChat);
    chatClose.addEventListener('click', toggleChat);

    // Send Message
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add User Message
        addMessage(message, 'user-message');
        chatInput.value = '';
        
        // Show Loading (Optional: could add a typing indicator)
        const loadingId = addMessage('Thinking...', 'bot-message', true);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // Remove loading message
            removeMessage(loadingId);

            if (data.response) {
                addMessage(data.response, 'bot-message');
            } else if (data.error) {
                addMessage('Error: ' + data.error, 'bot-message error');
            }
        } catch (error) {
            removeMessage(loadingId);
            addMessage('Error: Could not connect to server.', 'bot-message error');
            console.error('Chat Error:', error);
        }
    }

    chatSend.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function addMessage(text, className, isLoading=false) {
        const div = document.createElement('div');
        div.className = `message ${className}`;
        div.textContent = text;
        const id = 'msg-' + Date.now();
        div.id = id;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});
