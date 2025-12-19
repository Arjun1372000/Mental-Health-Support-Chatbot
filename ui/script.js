// Chat application JavaScript

const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');
const insightsBtn = document.getElementById('insightsBtn');
const modal = document.getElementById('insightsModal');
const closeModal = document.getElementById('closeModal');
const insightsContent = document.getElementById('insightsContent');

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
resetBtn.addEventListener('click', resetChat);
insightsBtn.addEventListener('click', showInsights);
closeModal.addEventListener('click', () => {
    modal.classList.remove('show');
});
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('show');
    }
});

// Send message to chatbot
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Add user message to UI
    addMessageToChat('user', message);
    userInput.value = '';
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (data.success) {
            // Add bot response
            addMessageToChat('bot', data.response);
            
            // Update emotion display
            updateEmotionDisplay({
                emotion: data.emotion,
                sentiment: data.sentiment,
                risk_level: data.risk_level
            });
        } else {
            addMessageToChat('bot', 'Sorry, I encountered an error. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingId);
        addMessageToChat('bot', 'Sorry, I encountered an error. Please try again.');
    }
}

// Add message to chat UI
function addMessageToChat(role, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role === 'user' ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = id;
    messageDiv.className = 'message bot-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<span class="typing">typing...</span>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return id;
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

// Update emotion display
function updateEmotionDisplay(data) {
    document.getElementById('emotionValue').textContent = data.emotion || '-';
    document.getElementById('sentimentValue').textContent = 
        (data.sentiment !== undefined ? data.sentiment.toFixed(2) : '-');
    document.getElementById('riskValue').textContent = data.risk_level || '-';
    
    // Color code risk level
    const riskElement = document.getElementById('riskValue');
    riskElement.style.background = getRiskColor(data.risk_level);
}

// Get color for risk level
function getRiskColor(riskLevel) {
    switch(riskLevel) {
        case 'LOW':
            return '#d4edda';
        case 'MODERATE':
            return '#fff3cd';
        case 'ELEVATED':
            return '#f8d7da';
        default:
            return '#f0f1f7';
    }
}

// Reset chat
async function resetChat() {
    if (!confirm('Are you sure you want to reset the conversation?')) return;
    
    try {
        const response = await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Clear chat messages
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-content">
                        <p>Hello! I'm here to listen and support you. Feel free to share how you're feeling today. Remember, this is a safe space.</p>
                    </div>
                </div>
            `;
            
            // Reset emotion display
            document.getElementById('emotionValue').textContent = '-';
            document.getElementById('sentimentValue').textContent = '-';
            document.getElementById('riskValue').textContent = '-';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to reset chat');
    }
}

// Show insights
async function showInsights() {
    modal.classList.add('show');
    insightsContent.innerHTML = '<p>Loading insights...</p>';
    
    try {
        const response = await fetch('/api/insights');
        const data = await response.json();
        
        if (data.success) {
            displayInsights(data);
        } else {
            insightsContent.innerHTML = '<p>Could not load insights. Please try again.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
        insightsContent.innerHTML = '<p>Error loading insights. Please try again.</p>';
    }
}

// Display insights
function displayInsights(data) {
    const basic = data.basic || {};
    const risk = data.risk || {};
    const recent = data.recent || {};
    
    let html = `
        <div>
            <h3>Basic Insights</h3>
            <p><strong>Total Days:</strong> ${basic.total_days || 0}</p>
            <p><strong>Average Sentiment:</strong> ${(basic.avg_sentiment || 0).toFixed(2)}</p>
            <p><strong>Most Common Emotion:</strong> ${basic.most_common_emotion || 'N/A'}</p>
            <p><strong>Max Sadness Streak:</strong> ${basic.max_sadness_streak || 0}</p>
        </div>
    `;
    
    if (risk && risk.risk_distribution) {
        html += `
            <div>
                <h3>Risk Insights</h3>
                <p><strong>Elevated Days:</strong> ${risk.elevated_days || 0}</p>
                <p><strong>Risk Distribution:</strong></p>
                <ul>
        `;
        for (const [level, count] of Object.entries(risk.risk_distribution || {})) {
            html += `<li>${level}: ${count}</li>`;
        }
        html += `</ul></div>`;
    }
    
    if (recent) {
        html += `
            <div>
                <h3>Recent Trend (Last 7 Days)</h3>
                <p><strong>Average Recent Sentiment:</strong> ${(recent.avg_recent_sentiment || 0).toFixed(2)}</p>
                <p><strong>Dominant Emotion:</strong> ${recent.dominant_emotion_last_7_days || 'N/A'}</p>
                <p><strong>Average Sadness Streak:</strong> ${(recent.avg_sadness_streak_last_7_days || 0).toFixed(2)}</p>
            </div>
        `;
    }
    
    insightsContent.innerHTML = html;
}

// Focus on input when page loads
window.addEventListener('load', () => {
    userInput.focus();
});
