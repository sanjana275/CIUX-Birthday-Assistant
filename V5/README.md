
# CIUX Birthday Assistant — Version 5

**GM University · School of Computer Science and Technology**  
**Course:** UE24CS3540 — Conversational Interfaces and UX  
**Faculty:** Dr. Shivanagowda G. M. and Tejas

## 1. Project Overview

Version 5 extends the Gemini-assisted, context-aware Birthday Assistant with browser-based voice interaction.

Users can interact with the chatbot using either text or speech. The browser Speech Recognition API converts spoken questions into text, which is processed by the existing Gemini-assisted NLU and deterministic rule engine.

The browser Speech Synthesis API reads chatbot responses aloud while preserving the normal text response.

The V5 backend, Gemini integration, dataset, dialogue management and deterministic factual processing are inherited from V4 and remain unchanged.

## 2. Learning Objectives

By the end of V5, students should be able to explain:

- Browser-based speech recognition.
- Browser-based speech synthesis.
- Voice-enabled conversational interfaces.
- Integration of JavaScript Web Speech APIs.
- Speech recognition using the en-IN language setting.
- Connecting voice input to an existing Flask chatbot.
- Providing both visual and spoken responses.
- Designing accessible multimodal interactions.

## 3. What's New in V5?

1. **Voice Input:** Users can ask questions through a microphone.
2. **Speech Recognition:** Browser speech recognition converts speech into text.
3. **Indian English Setting:** Uses `en-IN` for speech recognition.
4. **Voice Output:** Chatbot responses are spoken using Speech Synthesis.
5. **Voice Toggle:** Users can enable or disable spoken responses.
6. **Text Chat Support:** Users can continue typing questions normally.
7. **Context Preservation:** Existing V3 dialogue management remains available.
8. **Gemini Integration:** Existing V4 Gemini-assisted NLU is retained.
9. **Reset Conversation:** Users can clear the stored conversation context.
10. **Processing Trace:** Displays the chatbot's intent, entities and processing steps.

## 4. System Architecture

```text
User
 |
 |--------------------------|
 |                          |
Text Input              Voice Input
 |                          |
 |                    Browser Speech
 |                    Recognition API
 |                          |
 |                    Recognized Text
 |                          |
 |--------------------------|
             |
             v
       Flask Application
             |
             v
      Gemini-Assisted NLU
             |
             v
    Intent and Entity Extraction
             |
             v
      Entity Validation
             |
             v
    V3 Dialogue Management
             |
             v
   V1 Deterministic Rule Engine
             |
             v
       Excel Dataset
             |
             v
      Factual Response
             |
       |-------------|
       |             |
       v             v
   Text Display   Speech Synthesis
                  API (Browser)
```

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10 | Backend programming |
| Flask | Web application and API |
| Google Gemini API | LLM-assisted NLU |
| google-genai | Gemini Python SDK |
| python-dotenv | Environment variable management |
| Pandas | Dataset processing |
| Excel | Birthday information storage |
| HTML | Chatbot interface |
| CSS | Interface styling |
| JavaScript | Frontend interaction |
| Web Speech API | Browser speech recognition and synthesis |
| Pytest | Automated testing |

## 6. Project Structure

```text
V5/
├── app.py
├── data_service.py
├── dialogue.py
├── llm_nlu.py
├── nlu.py
├── service.py
├── rules.py
├── requirements.txt
├── README.md
├── .env
├── data/
│   └── people.xlsx
├── templates/
│   └── index.html
├── static/
│   ├── chat.js
│   └── style.css
└── tests/
    ├── test_dialogue.py
    ├── test_nlu.py
    └── test_rules.py
```

The `.env` file stores the Gemini API configuration and must never be committed to GitHub.

## 7. Setup on Windows / VS Code

Open the V5 project folder in VS Code.

### Step 1: Create a virtual environment

```powershell
py -3.10 -m venv .venv
```

### Step 2: Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure Gemini API

Create a `.env` file inside the V5 folder.

Add:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder with your own Gemini API key.

Never upload the `.env` file or expose the API key in source code.

### Step 5: Run the application

```powershell
python app.py
```

Open the application:

http://127.0.0.1:5000

## 8. Voice Interaction

### Voice Input

1. Open the chatbot in a supported browser.
2. Click the **Speak** button.
3. Allow microphone permission.
4. Ask a birthday-related question.
5. The browser converts speech into text.
6. The recognized text is submitted to the existing chatbot backend.

### Voice Output

1. Submit a question using text or voice.
2. The chatbot displays its answer.
3. The browser reads the response aloud.
4. Use the Voice On/Off button to control spoken responses.

### Browser Compatibility

Speech recognition availability depends on browser support. Google Chrome and Microsoft Edge are suitable browsers to test this project.

Microphone access requires user permission. Use localhost or a secure HTTPS connection.

If speech recognition is unavailable, normal text interaction remains available.

## 9. Example Questions

```text
Hello

When is Appa's birthday?

When is Rahul's birthday?

How many birthdays are in September?

Any nephew birthdays in September?

What about October?

Where does Lakshmi live?

How old is Raghavendra Gowda?

Who has birthdays tomorrow?
```

Questions can be entered using either the keyboard or microphone.

For ambiguous names, the chatbot asks the user to clarify which person they mean.

## 10. Testing

Run the automated tests:

```powershell
python -m pytest -v
```

The inherited automated test suite covers:

- Dialogue management.
- Context and follow-up questions.
- Clarification handling.
- Intent recognition.
- Entity extraction.
- Deterministic rule processing.

Record the final test results after running the complete suite.

Manual voice testing should cover:

- Microphone permission.
- Speech recognition.
- Correct recognized text.
- Spoken chatbot responses.
- Voice on/off control.
- Normal text chat.
- Conversation reset.

## 11. Important Design Principle

**Voice is an additional interaction method; it does not replace the existing chatbot intelligence.**

Speech recognition converts voice into text. Gemini understands the question, and the deterministic rule engine retrieves factual information. Speech synthesis reads the final response aloud.

The LLM does not independently generate birthday dates or invent information.

## 12. Privacy and Security

The included dataset contains synthetic records.

- Keep API keys inside `.env`.
- Never commit `.env` to GitHub.
- Do not expose real personal birthday information.
- Microphone access requires user permission.
- Use synthetic data for academic demonstrations.

## 13. Version History

| Version | Main Feature |
|---|---|
| V1 | Deterministic rule-based chatbot |
| V2 | Intent recognition and entity extraction |
| V3 | Context-aware dialogue management |
| V4 | Gemini-assisted natural language understanding |
| V5 | Browser-based voice interaction |
