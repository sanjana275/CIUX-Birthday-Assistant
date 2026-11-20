
from datetime import date
import calendar

from nlu import understand_message
from rules import answer_question
from dialogue import DialogueManager


def process_message(people, message, context=None, today=None):
    """
    V3 service:
    1. Recognizes intent and entities.
    2. Maintains conversation context.
    3. Handles follow-up questions.
    4. Clarifies ambiguous person names.
    5. Uses the existing deterministic V1 rule engine.
    """

    today = today or date.today()

    manager = DialogueManager(context)
    message = (message or "").strip()

    if not message:
        return {
            "answer": "Please type a question.",
            "trace": ["V3 dialogue engine"],
            "context": manager.get_context()
        }

    result = understand_message(message, people)

    intent = result["intent"]
    entities = result["entities"]

    current_context = manager.get_context()

    trace = [
        "V3 engine: Context-aware dialogue management",
        f"Recognized intent: {intent}",
        f"Extracted entities: {entities}"
    ]

    # Handle an existing clarification.
    pending = current_context.get("pending_clarification")

    if pending:
        candidates = pending.get("candidates", [])

        selected = [
            name for name in candidates
            if name.lower() in message.lower()
        ]

        if len(selected) != 1:
            names = "\n".join(
                f"- {name}" for name in candidates
            )

            return {
                "answer": (
                    "I still need to know which person you mean. "
                    "Please choose one of these names:\n" + names
                ),
                "trace": trace + ["Waiting for person clarification"],
                "context": manager.get_context()
            }

        original_question = pending.get("question", "")
        message = original_question + " " + selected[0]

        manager.clear_clarification()

        resolved_result = understand_message(message, people)
        intent = resolved_result["intent"]
        entities = resolved_result["entities"]

        trace.append(f"Clarification resolved: {selected[0]}")

    # Ask for clarification when a nickname matches multiple people.
    candidates = entities.get("person_candidates", [])

    if len(candidates) > 1:
        manager.set_clarification({
            "type": "person",
            "question": message,
            "candidates": candidates
        })

        names = "\n".join(
            f"- {name}" for name in candidates
        )

        return {
            "answer": (
                "I found multiple people matching that name. "
                "Who are you asking about?\n" + names
            ),
            "trace": trace + ["Ambiguous person: clarification requested"],
            "context": manager.get_context()
        }

    # Detect follow-up questions.
    follow_up = message.lower().startswith(
        ("what about", "how about", "and ", "also ", "then ")
    )

    previous_intent = current_context.get("last_intent")
    previous_month = current_context.get("month")
    previous_relationship = current_context.get("relationship")

    month = entities.get("month")
    relationship = entities.get("relationship")

    effective_intent = intent

    # Reuse previous intent for month-only follow-ups.
    if (
        intent == "unknown"
        and month is not None
        and previous_intent in ["birthday_count", "birthday_lookup"]
    ):
        effective_intent = previous_intent
        trace.append("Context: Previous intent reused")

    # Reuse context only for genuine follow-up questions.
    if follow_up:
        if month is None:
            month = previous_month

        if relationship is None:
            relationship = previous_relationship

    # Build a question understood by the deterministic rule engine.
    rule_question = message

    if effective_intent == "birthday_lookup":
        person_name = entities.get("person_name")

        if person_name:
            rule_question = f"When is {person_name}'s birthday?"

        elif month:
            rule_question = (
                "birthdays in " + calendar.month_name[month]
            )

            if relationship:
                rule_question += " " + relationship

    elif effective_intent == "birthday_count":
        rule_question = "how many birthdays"

        if relationship:
            rule_question += " " + relationship

        if month:
            rule_question += " in " + calendar.month_name[month]

    elif effective_intent == "upcoming_birthdays":
        rule_question = message

        if relationship:
            rule_question += " " + relationship

    # Handle greetings, help and unsupported questions.
    if intent == "greeting":
        response = {
            "answer": (
                "Hello! Welcome to Birthday Assistant V3. "
                "I can remember details from our conversation "
                "and answer follow-up questions."
            ),
            "trace": []
        }

    elif intent == "help":
        response = {
            "answer": (
                "You can ask me questions such as:\n"
                "- When is Rahul's birthday?\n"
                "- How many birthdays are in September?\n"
                "- What about October?\n"
                "- Who has birthdays tomorrow?\n"
                "- When is my mother's birthday?\n"
                "- Where does Rahul stay?"
            ),
            "trace": []
        }

    elif effective_intent == "unknown":
        response = {
            "answer": (
                "Sorry, I could not understand your question. "
                "Try asking about birthdays, people, relationships or places."
            ),
            "trace": []
        }

    else:
        response = answer_question(
            people,
            rule_question,
            today=today
        )

    # Save updated conversation context.
    if effective_intent != "unknown":
        manager.update_context(
            intent=effective_intent,
            entities={
                "month": entities.get("month") or month,
                "relationship": entities.get("relationship") or relationship,
                "person_name": entities.get("person_name")
            }
        )

    trace.append(f"Effective intent: {effective_intent}")
    trace.append(f"Context used: {manager.get_context()}")

    return {
        "answer": response["answer"],
        "trace": trace + response.get("trace", []),
        "context": manager.get_context()
    }
