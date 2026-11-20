
const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const question = document.getElementById('question');
const trace = document.getElementById('trace');
const resetButton = document.getElementById('reset-chat');

const voiceInputButton = document.getElementById('voice-input');
const voiceOutputButton = document.getElementById('voice-output');
const voiceStatus = document.getElementById('voice-status');

let voiceEnabled = true;
let recognition = null;
let isListening = false;

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

// Speak the chatbot response.
function speakResponse(text) {
  if (!voiceEnabled || !('speechSynthesis' in window)) {
    return;
  }

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-IN';
  utterance.rate = 1;
  utterance.pitch = 1;

  window.speechSynthesis.speak(utterance);
}

// Send a message to the existing Flask backend.
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
    const answer = data.answer || 'No answer returned.';

    addMessage(answer, 'bot');
    speakResponse(answer);

    trace.textContent = (data.trace || [])
      .map((x, i) => `${i + 1}. ${x}`)
      .join('\n');

  } catch (error) {
    const message = `Error: ${error.message}`;
    addMessage(message, 'bot');
    speakResponse(message);

  } finally {
    question.disabled = false;
    question.focus();
  }
}

// Normal text submission.
form.addEventListener('submit', e => {
  e.preventDefault();
  ask(question.value);
});

// Example questions.
document.querySelectorAll('.chip[data-q]').forEach(button => {
  button.addEventListener('click', () => ask(button.dataset.q));
});

// Reset conversation.
resetButton.addEventListener('click', async () => {
  resetButton.disabled = true;

  if (recognition && isListening) {
    recognition.stop();
  }

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }

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
    speakResponse(data.answer);

  } catch (error) {
    addMessage(`Reset failed: ${error.message}`, 'bot');

  } finally {
    resetButton.disabled = false;
    question.focus();
  }
});

// Initialize browser speech recognition.
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();

  recognition.lang = 'en-IN';
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    isListening = true;
    voiceInputButton.textContent = '🔴 Listening...';
    voiceStatus.textContent = 'Listening. Please speak your question.';
  };

  recognition.onresult = event => {
    const spokenText = event.results[0][0].transcript;

    question.value = spokenText;
    voiceStatus.textContent = `Recognized: ${spokenText}`;

    // Send recognized speech through the existing chat function.
    ask(spokenText);
  };

  recognition.onerror = event => {
    voiceStatus.textContent =
      `Voice recognition error: ${event.error}. Please try again.`;
  };

  recognition.onend = () => {
    isListening = false;
    voiceInputButton.textContent = '🎤 Speak';
  };

} else {
  voiceInputButton.disabled = true;
  voiceStatus.textContent =
    'Speech recognition is not supported in this browser. Try Microsoft Edge or Google Chrome.';
}

// Microphone button.
voiceInputButton.addEventListener('click', () => {
  if (!recognition) return;

  if (isListening) {
    recognition.stop();
    return;
  }

  try {
    recognition.start();
  } catch (error) {
    voiceStatus.textContent =
      'Could not start microphone. Please try again.';
  }
});

// Voice output on/off.
voiceOutputButton.addEventListener('click', () => {
  voiceEnabled = !voiceEnabled;

  voiceOutputButton.textContent = voiceEnabled
    ? '🔊 Voice: On'
    : '🔇 Voice: Off';

  voiceOutputButton.setAttribute('aria-pressed', String(voiceEnabled));

  if (!voiceEnabled && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }

  voiceStatus.textContent = voiceEnabled
    ? 'Spoken responses enabled.'
    : 'Spoken responses disabled. Text chat is still available.';
});

// V5 welcome message.
addMessage(
  "Hello! Welcome to the V5 Voice-Enabled Gemini Birthday Assistant 🎂\n\n" +
  "You can type your questions or press the Speak button to ask using your microphone.\n\n" +
  "I can understand natural language questions, remember conversation context, and retrieve birthday information from the dataset.\n\n" +
  "Try asking:\n" +
  "- When is Appa's birthday?\n" +
  "- How many birthdays are in September?\n" +
  "- Where does Lakshmi live?"
);
