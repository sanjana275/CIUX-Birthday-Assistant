
from flask import Flask, jsonify, render_template, request

from data_service import load_people
from service import process_message

app = Flask(__name__)

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

    result = process_message(PEOPLE, message)

    return jsonify(result)


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        records=len(PEOPLE),
        version="V2"
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
