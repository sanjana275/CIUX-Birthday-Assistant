# CIUX Birthday Assistant — Version 1

**GM University · School of Computer Science and Technology**  
**Course:** UE24CS3540 — Conversational Interfaces and UX  
**Faculty:** Dr. Shivanagowda G. M. and Tejas

Version 1 is intentionally **deterministic**. It does not use an LLM, ML model, vector database, or RAG. Students can inspect every rule that turns a user utterance into a spreadsheet filter and a response.

## Learning target

By the end of V1, you should be able to explain this pipeline:

`Question → phrase/rule matching → filter construction → Pandas/Excel lookup → response template`

You should also be able to identify why a rigid rule-based interface fails when users paraphrase requests in unexpected ways. That limitation motivates V2.

## Project structure

```text
CIUX_Birthday_Assistant_V1/
├── app.py                 Flask routes
├── data_service.py        Excel loading + validation
├── rules.py               deterministic conversation rules
├── requirements.txt
├── data/
│   └── people.xlsx        100 fictional records
├── templates/
│   └── index.html
├── static/
│   ├── chat.js
│   └── style.css
└── tests/
    └── test_rules.py
```

## Setup on Windows / VS Code

Open the project folder in VS Code, then open **Terminal → New Terminal**.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:5000`

If PowerShell blocks activation, either use Command Prompt with `.venv\Scripts\activate.bat`, or run the venv interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

## Questions V1 is designed to handle

```text
What are the upcoming birthdays?
How many birthdays are there next month?
Is there any birthday tomorrow?
When is my wife's birthday?
Any nephew birthdays in September?
Who has birthdays this week?
When is Rahul Patil's birthday?
How old is Rahul Patil?
Who stays in Bengaluru?
```

The **Rule Trace** panel in the browser is part of the teaching design. Ask students to inspect it after every question.

## Run the tests

```powershell
pytest -q
```

## V1 exploration tasks

1. Add a rule for `day after tomorrow`.
2. Add aliases such as `bro`, `sis`, or a local-language family term.
3. Add a query for `birthdays within 10 days`.
4. Intentionally ask five paraphrases that V1 cannot understand.
5. Record why each failed. Do not repair all of them yet — these failures become requirements for V2.

## Important privacy note

The included 100-person dataset is synthetic. When using a real family/contact dataset, do not commit it to a public Git repository.
