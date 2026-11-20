# CIUX Birthday Assistant — Version 4

**GM University · School of Computer Science and Technology**  
**Course:** UE24CS3540 — Conversational Interfaces and UX  
**Faculty:** Dr. Shivanagowda G. M. and Tejas

## Project Overview

Version 4 extends the context-aware Birthday Assistant by integrating **Google Gemini for Large Language Model (LLM)-assisted Natural Language Understanding (NLU)**.

The system uses Gemini to understand natural language questions, identify user intents and extract relevant entities. Extracted information is validated against the Excel dataset before being passed to the existing dialogue management and deterministic rule-processing system.

Gemini is used only for understanding user messages. Actual birthday information is retrieved from the Excel dataset using deterministic rules to ensure factual accuracy.

## Learning Objectives

By the end of V4, you should be able to explain:

- LLM-assisted intent recognition and entity extraction.
- Integration of Google Gemini API with a Python Flask application.
- Structured JSON output from an LLM.
- Validation of extracted person names against an Excel dataset.
- Combining LLM-based NLU with deterministic rule-based processing.
- Fallback to deterministic NLU when Gemini is unavailable.
- Context-aware dialogue and clarification handling.

## What's New in V4?

1. **Gemini Integration:** Uses Google Gemini for natural language understanding.
2. **Intent Recognition:** Identifies greeting, help, birthday lookup, birthday count, upcoming birthdays, age lookup and place lookup.
3. **Entity Extraction:** Extracts person names, relationships, months and places.
4. **Person Validation:** Matches Gemini-extracted names against the Excel dataset.
5. **Month Normalization:** Converts month names into numeric values for deterministic processing.
6. **Relationship Normalization:** Converts extracted relationship values into the dataset's standard format.
7. **Context Management:** Reuses V3 dialogue management for follow-up questions and clarification.
8. **Deterministic Factual Answers:** Uses the existing V1 rule engine to retrieve actual birthday information.
9. **Fallback Mechanism:** Uses deterministic V3 NLU if Gemini fails or is unavailable.
10. **Processing Trace:** Displays recognized intents, extracted entities and processing steps.

## System Architecture

```text
User Message
     |
     v
Flask Application
     |
     v
Gemini-Assisted NLU
     |
     v
Intent Recognition
     |
     v
Entity Extraction
     |
     v
Entity Validation and Normalization
     |
     v
V3 Dialogue Management
     |
     v
V1 Deterministic Rule Engine
     |
     v
Pandas / Excel Dataset
     |
     v
Factual Response
     |
     v
Chatbot Interface
```

If Gemini is unavailable, the system falls back to deterministic NLU.

## Technologies Used

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
| Pytest | Automated testing |

## Project Structure

```text
V4/
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

The `.env` file contains API configuration and must not be committed to GitHub.

## Setup on Windows / VS Code

Open the V4 project folder in VS Code.

### 1. Create a virtual environment

```powershell
py -3.10 -m venv .venv
```

### 2. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
python -m pip install google-genai python-dotenv
```

### 4. Configure Gemini API

Create a `.env` file inside the V4 folder.

Add:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder with your own Gemini API key.

Never upload the `.env` file or expose your API key in source code.

### 5. Run the application

```powershell
python app.py
```

Open the application:

http://127.0.0.1:5000

## Example Questions

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

For ambiguous names, the assistant asks the user to clarify which person they mean.

## Testing

Run the automated tests:

```powershell
python -m pytest -v
```

The test suite includes:

- Dialogue management tests.
- Context and follow-up tests.
- Clarification handling tests.
- Intent recognition tests.
- Entity extraction tests.
- Deterministic rule engine tests.

Record the final number of passed and failed tests after running the complete suite.

## Important Design Principle

**Gemini understands the question; the deterministic rule engine provides the factual answer.**

The LLM does not independently generate birthday dates or invent information. Person names are validated against the Excel dataset, and factual responses are retrieved through the existing deterministic processing system.

## Privacy and Security

The included dataset contains synthetic records.

- Keep API keys inside `.env`.
- Never commit `.env` to GitHub.
- Do not expose real personal birthday information in a public repository.
- Use synthetic data for demonstrations and academic submissions.

## Version History

| Version | Main Feature |
|---|---|
| V1 | Deterministic rule-based chatbot |
| V2 | Intent recognition and entity extraction |
| V3 | Context-aware dialogue management |
| V4 | Gemini-assisted natural language understanding |
| V5 | Browser-based voice interaction |
