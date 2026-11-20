
import os

from flask import Flask, jsonify, render_template, request, session

from data_service import load_people
from service import process_message

app = Flask(__name__)

# Secret key is used to protect Flask session data.
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "ciux-birthday-assistant-v3-development-key"
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

    # Retrieve previous conversation context.
    context = session.get("dialogue_context", {})

    result = process_message(
        PEOPLE,
        message,
        context=context
    )

    # Save updated context for the next message.
    session["dialogue_context"] = result.get("context", {})

    return jsonify(result)


@app.post("/api/reset")
def reset():
    # Clear conversation memory.
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
        version="V3"
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
