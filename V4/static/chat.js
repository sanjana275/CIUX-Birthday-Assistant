
const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const question = document.getElementById('question');
const trace = document.getElementById('trace');
const resetButton = document.getElementById('reset-chat');

function addMessage(text, role) {
  const row = document.createElement('div');
  row.className = `message ${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;

  row.appendChild(bubble);
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

async function ask(text) {
  text = text.trim();

  if (!text) return;

  addMessage(text, 'user');
  question.value = '';
  question.disabled = true;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    addMessage(data.answer || 'No answer returned.', 'bot');

    trace.textContent = (data.trace || [])
      .map((x, i) => `${i + 1}. ${x}`)
      .join('\n');

  } catch (error) {
    addMessage(`Error: ${error.message}`, 'bot');

  } finally {
    question.disabled = false;
    question.focus();
  }
}

// Send a message.
form.addEventListener('submit', e => {
  e.preventDefault();
  ask(question.value);
});

// Example question buttons.
document.querySelectorAll('.chip[data-q]').forEach(button => {
  button.addEventListener('click', () => ask(button.dataset.q));
});

// Reset conversation and clear stored context.
resetButton.addEventListener('click', async () => {
  resetButton.disabled = true;

  try {
    const response = await fetch('/api/reset', {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    chat.innerHTML = '';
    trace.textContent = 'Conversation context cleared.';

    addMessage(data.answer, 'bot');

  } catch (error) {
    addMessage(`Reset failed: ${error.message}`, 'bot');

  } finally {
    resetButton.disabled = false;
    question.focus();
  }
});


// V4 welcome message.
addMessage(
  "Hello! Welcome to the V4 Gemini-Assisted Birthday Assistant 🎂\n\n" +
  "I can understand natural language questions, remember conversation context, and find accurate birthday information from your family dataset.\n\n" +
  "Try asking:\n" +
  "- When is Appa's birthday?\n" +
  "- How many birthdays are in September?\n" +
  "- Where does Lakshmi live?"
);
