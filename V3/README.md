# CIUX Birthday Assistant — Version 2

**GM University · School of Computer Science and Technology**  
**Course:** UE24CS3540 — Conversational Interfaces and UX  
**Faculty:** Dr. Shivanagowda G. M. and Tejas

Version 2 extends the deterministic rule-based Birthday Assistant by introducing **Intent Recognition and Entity Extraction**.

The system identifies what the user wants to know (intent) and extracts relevant information (entities), such as a person's name, relationship, month or place. The recognized information is then used alongside the existing deterministic rule engine to retrieve factual answers from the Excel dataset.

V2 does not use an LLM, machine learning model, vector database or RAG.

## Learning target

By the end of V2, you should be able to explain this pipeline:

`User utterance → Intent recognition → Entity extraction → Deterministic rules → Pandas/Excel lookup → Response template`

You should understand the difference between identifying the user's intention and extracting important information from the utterance.

You should also be able to compare V1's explicit phrase matching with V2's intent and entity recognition approach.

## What's new in V2?

1. **Intent Recognition:** Identifies the purpose of the user's question, such as birthday lookup, birthday count, upcoming birthdays, age lookup, place lookup, greeting and help.
2. **Entity Extraction:** Identifies relevant information, including person names, relationships, months and places.
3. **Processing Trace:** Displays the recognized intent and extracted entities.
4. **Existing Rule Engine:** Reuses the deterministic V1 rules to retrieve factual information from the dataset.
5. **Greeting and Help:** Provides dedicated responses for greetings and help requests.

## Project structure

```text
V2/
├── app.py                 Flask application and API routes
├── data_service.py        Excel loading and validation
├── nlu.py                 Intent recognition and entity extraction
├── service.py             Message processing and service logic
├── rules.py               Deterministic conversation rules
├── requirements.txt
├── data/
│   └── people.xlsx        100 synthetic records
├── templates/
│   └── index.html         Chatbot interface
├── static/
│   ├── chat.js            Frontend interaction
│   └── style.css          Interface styling
└── tests/
    ├── test_nlu.py        NLU tests
    └── test_rules.py      Rule engine tests
```

## Setup on Windows / VS Code

Open the V2 project folder in VS Code and select **Terminal → New Terminal**.

Create and activate a virtual environment if you have not already created one:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python app.py
```

Open the application:

http://127.0.0.1:5000

If PowerShell activation causes problems, use the virtual environment interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

## Questions V2 is designed to handle

```text
Hello
When is Rahul Patil's birthday?
When is my mother's birthday?
How many birthdays are in September?
Who has birthdays tomorrow?
What are the upcoming birthdays?
Where does Rahul stay?
How old is Rahul Patil?
```

The **Processing Trace** panel displays the recognized intent, extracted entities and deterministic processing steps.

## Run the tests

Run the automated tests from the V2 folder:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

### Current test results

**13 tests passed**

- 7 tests for intent recognition and entity extraction.
- 6 tests for the existing deterministic rule engine.

## V2 exploration tasks

1. Try different ways of asking the same birthday question.
2. Test whether the system correctly recognizes names and nicknames.
3. Test relationship and month entity extraction.
4. Identify questions where the intent is recognized but the entity is missing.
5. Compare V1 and V2 responses to the same questions.
6. Record cases where the system still fails to understand the user's wording.

## Important privacy note

The included 100-person dataset is synthetic. When using a real family or contact dataset, do not commit it to a public Git repository.