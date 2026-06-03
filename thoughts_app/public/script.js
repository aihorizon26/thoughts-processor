// Configuration: set this to your deployed backend URL
// For local development, use: http://localhost:5000
const API_URL = ""; // <-- Fill in after deployment, e.g., "https://thoughts-processor.vercel.app"

const thoughtsList = document.getElementById('thoughts-list');
const thoughtInput = document.getElementById('thought-input');
const processBtn = document.getElementById('process-btn');
const voiceBtn = document.getElementById('voice-btn');
const feedbackEl = document.getElementById('feedback');
const sortSelect = document.getElementById('sort-select');

let thoughts = [];

// Fetch thoughts from backend
async function fetchThoughts() {
    try {
        const order = sortSelect.value === 'roi' ? '?order=roi.desc' : '';
        const response = await fetch(`${API_URL}/api/thoughts${order}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        thoughts = await response.json();
        renderThoughts();
    } catch (err) {
        console.error('Failed to fetch thoughts:', err);
        showFeedback('Error loading thoughts', 'error');
    }
}

// Render thoughts as cards
function renderThoughts() {
    thoughtsList.innerHTML = '';
    if (thoughts.length === 0) {
        thoughtsList.innerHTML = '<p class="empty-state">No thoughts yet. Add one above!</p>';
        return;
    }
    thoughts.forEach(t => {
        const card = document.createElement('div');
        card.className = 'thought-card';
        const timestamp = new Date(t.created_at).toLocaleString();
        card.innerHTML = `
            <div class="thought-header">
                <span class="roi-badge">${t.roi}</span>
                <span class="classification-tag">${t.classification}</span>
            </div>
            <div class="thought-body">${escapeHtml(t.thought)}</div>
            <div class="thought-footer">${timestamp}</div>
        `;
        thoughtsList.appendChild(card);
    });
}

// Simple XSS escape
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Show feedback message
function showFeedback(message, type) {
    feedbackEl.textContent = message;
    feedbackEl.className = `feedback ${type}`;
    feedbackEl.style.display = 'block';
    setTimeout(() => {
        feedbackEl.style.display = 'none';
    }, 3000);
}

// Process a new thought
async function processThought() {
    const raw = thoughtInput.value.trim();
    if (!raw) {
        showFeedback('Please enter a thought', 'error');
        return;
    }
    processBtn.disabled = true;
    processBtn.textContent = 'Processing…';
    try {
        const response = await fetch(`${API_URL}/api/thoughts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ thought: raw })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result = await response.json();
        showFeedback(`Saved! ROI: ${result.roi} • ${result.classification}`, 'success');
        thoughtInput.value = '';
        await fetchThoughts(); // refresh list
    } catch (err) {
        console.error('Failed to add thought:', err);
        showFeedback('Error saving thought', 'error');
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = 'Process with Claude Council';
    }
}

// Voice simulation (for demo)
function simulateVoice() {
    const voicePrompt = "Say your thought now (simulated): ";
    const spoken = prompt(voicePrompt, '');
    if (spoken !== null) {
        thoughtInput.value = spoken.trim();
        processBtn.focus();
    }
}

// Event listeners
processBtn.addEventListener('click', processThought);
voiceBtn.addEventListener('click', simulateVoice);
thoughtInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        e.preventDefault();
        processThought();
    }
});
sortSelect.addEventListener('change', fetchThoughts);

// Initial load
fetchThoughts();
