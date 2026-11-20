
from datetime import date
import calendar

from nlu import understand_message
from rules import answer_question


def process_message(people, message, today=None):
    """
    V2 service:
    1. Understand the user's message.
    2. Identify intent and entities.
    3. Use the existing birthday rules to retrieve factual answers.
    """

    today = today or date.today()

    result = understand_message(message, people)

    intent = result["intent"]
    entities = result["entities"]

    trace = [
        "V2 engine: Intent and Entity Recognition",
        f"Recognized intent: {intent}",
        f"Extracted entities: {entities}"
    ]

    if not message or not message.strip():
        return {
            "answer": "Please type a question.",
            "trace": trace
        }

    if intent == "greeting":
        return {
            "answer": "Hello! Welcome to Birthday Assistant V2. You can ask me about birthdays, people, relationships and places.",
            "trace": trace
        }

    if intent == "help":
        return {
            "answer": (
                "You can ask me questions such as:\n"
                "• When is Rahul's birthday?\n"
                "• How many birthdays are in September?\n"
                "• Who has birthdays tomorrow?\n"
                "• When is my mother's birthday?\n"
                "• Where does Rahul stay?"
            ),
            "trace": trace
        }

    if intent == "unknown":
        return {
            "answer": (
                "Sorry, I could not understand your question. "
                "Try asking about a person's birthday, a month, or a relationship."
            ),
            "trace": trace
        }

    # Pass recognized information to the existing V1 rule engine.
    response = answer_question(people, message, today=today)

    return {
        "answer": response["answer"],
        "trace": trace + response.get("trace", [])
    }
