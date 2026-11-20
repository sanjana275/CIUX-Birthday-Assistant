
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

from data_service import load_people
from service import process_message

# Load V4 environment variables.
load_dotenv(Path(__file__).resolve().parent / ".env")

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "ciux-birthday-assistant-v4-development-key"
)

PEOPLE = load_people()


@app.get("/")
def index():
    return render_template(
        "index.html",
        record_count=len(PEOPLE)
    )


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")

    context = session.get("dialogue_context", {})

    result = process_message(
        PEOPLE,
        message,
        context=context
    )

    session["dialogue_context"] = result.get("context", {})

    return jsonify(result)


@app.post("/api/reset")
def reset():
    session.pop("dialogue_context", None)

    return jsonify({
        "answer": "Conversation reset. Let's start again!",
        "status": "success"
    })


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        records=len(PEOPLE),
        version="V4",
        nlu="Gemini-assisted"
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
