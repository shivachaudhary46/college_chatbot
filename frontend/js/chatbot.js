 // Configuration
        const API_BASE_URL = 'http://localhost:8000'; // Change to your API URL
        const CHAT_ENDPOINT = '/api/v1/chat/'; // Must match FastAPI route with trailing slash

        // Enhanced token retrieval function - checks multiple possible locations
        function getAuthToken() {
            // Check multiple possible token storage locations
            const possibleKeys = [
                'access_token',
                'token',
                'auth_token',
                'jwt',
                'authToken',
                'accessToken'
            ];

            for (const key of possibleKeys) {
                const token = localStorage.getItem(key);
                if (token) {
                    console.log(`Token found in localStorage with key: ${key}`);
                    return token;
                }
            }

            // Check sessionStorage
            for (const key of possibleKeys) {
                const token = sessionStorage.getItem(key);
                if (token) {
                    console.log(`Token found in sessionStorage with key: ${key}`);
                    return token;
                }
            }

            // Check cookies
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (possibleKeys.includes(name)) {
                    console.log(`Token found in cookie with name: ${name}`);
                    return value;
                }
            }

            console.warn('No authentication token found!');
            return null;
        }

        // Debug function to show all storage
        function showDebugInfo() {
            const debugDiv = document.getElementById('debugInfo');
            
            console.log('=== DEBUGGING TOKEN STORAGE ===');
            console.log('LocalStorage:', { ...localStorage });
            console.log('SessionStorage:', { ...sessionStorage });
            console.log('Cookies:', document.cookie);
            
            const token = getAuthToken();
            
            debugDiv.innerHTML = `
                <div class="debug-info">
                    <strong>Debug Info:</strong><br>
                    Token found: ${token ? 'YES ✓' : 'NO ✗'}<br>
                    ${token ? `Token preview: ${token.substring(0, 20)}...` : 'No token in storage'}<br>
                    <button onclick="console.log('Full localStorage:', localStorage); console.log('Full token:', getAuthToken())">
                        Log Full Details
                    </button>
                    <button onclick="document.getElementById('debugInfo').style.display='none'">
                        Hide Debug
                    </button>
                </div>
            `;
        }

        // DOM Elements
        const chatbotToggle = document.getElementById('chatbotToggle');
        const chatbotWidget = document.getElementById('chatbotWidget');
        const closeChatbot = document.getElementById('closeChatbot');
        const chatMessages = document.getElementById('chatMessages');
        const chatForm = document.getElementById('chatForm');
        const userInput = document.getElementById('userInput');
        const sendButton = document.getElementById('sendButton');

        // Show debug info on load
        window.addEventListener('load', () => {
            showDebugInfo();
        });

        // Toggle chatbot
        chatbotToggle.addEventListener('click', () => {
            chatbotWidget.classList.add('active');
            chatbotToggle.style.display = 'none';
            userInput.focus();
        });

        closeChatbot.addEventListener('click', () => {
            chatbotWidget.classList.remove('active');
            chatbotToggle.style.display = 'flex';
        });

        // Add message
        function addMessage(content, isBot = false, queryType = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isBot ? 'bot' : 'user'}`;
            
            const time = new Date().toLocaleTimeString('en-US', { 
                hour: 'numeric', 
                minute: '2-digit' 
            });
            
            if (isBot) {
                messageDiv.innerHTML = `
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-bubble">
                            ${content}
                            ${queryType ? `<br><span class="query-type-badge">${queryType}</span>` : ''}
                        </div>
                        <div class="message-time">${time}</div>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="message-content">
                        <div class="message-bubble">${content}</div>
                        <div class="message-time">${time}</div>
                    </div>
                `;
            }
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Typing indicator
        function showTypingIndicator() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot typing-indicator';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = `
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            `;
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function removeTypingIndicator() {
            const typingIndicator = document.getElementById('typingIndicator');
            if (typingIndicator) typingIndicator.remove();
        }

        // Send message
        async function sendMessage(query) {
            const token = getAuthToken();
            
            if (!token) {
                addMessage('⚠️ No authentication token found. Please login first.', true);
                console.error('No token available. Check localStorage, sessionStorage, or cookies.');
                return;
            }
            
            //.substring(0, 20)
            console.log('Sending request with token:', token + '...');
            
            try {
                showTypingIndicator();
                
                const response = await fetch(`${API_BASE_URL}${CHAT_ENDPOINT}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ query: query })
                });
                
                removeTypingIndicator();
                
                console.log('Response status:', response.status);
                
                if (response.status === 401) {
                    const errorData = await response.json().catch(() => ({}));
                    console.error('401 Unauthorized:', errorData);
                    addMessage('⚠️ Authentication failed. Your session may have expired. Please login again.', true);
                    return;
                }
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    console.error('API Error:', errorData);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                console.log('Success! Response:', data);
                addMessage(data.response, true, data.query_type);
                
            } catch (error) {
                removeTypingIndicator();
                console.error('Error sending message:', error);
                addMessage('⚠️ Failed to get response. Check console for details.', true);
            }
        }

        // Handle form submission
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const query = userInput.value.trim();
            if (!query) return;
            
            addMessage(query, false);
            userInput.value = '';
            
            userInput.disabled = true;
            sendButton.disabled = true;
            
            await sendMessage(query);
            
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        });

        // Make getAuthToken available globally for debugging
        window.getAuthToken = getAuthToken;
        window.showDebugInfo = showDebugInfo;