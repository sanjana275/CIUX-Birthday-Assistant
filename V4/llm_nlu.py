
import calendar
import json
import os
import traceback
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from nlu import understand_message


# Load API key and model from V4/.env
load_dotenv(Path(__file__).resolve().parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

ALLOWED_INTENTS = {
    "greeting",
    "help",
    "place_lookup",
    "age_lookup",
    "birthday_count",
    "upcoming_birthdays",
    "birthday_lookup",
    "unknown",
}

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "intent": {
            "type": "STRING",
            "enum": sorted(ALLOWED_INTENTS),
        },
        "entities": {
            "type": "OBJECT",
            "properties": {
                "person_name": {"type": ["STRING", "NULL"]},
                "relationship": {"type": ["STRING", "NULL"]},
                "month": {"type": ["STRING", "NULL"]},
                "place": {"type": ["STRING", "NULL"]},
            },
            "required": [
                "person_name",
                "relationship",
                "month",
                "place",
            ],
        },
    },
    "required": ["intent", "entities"],
}


def normalize_person_name(name, people):
    """Match Gemini's person name against the Excel dataset."""

    if not name:
        return None, []

    query = str(name).strip().casefold()
    candidates = []

    # Support both Pandas DataFrames and lists of dictionaries.
    if hasattr(people, "to_dict"):
        records = people.to_dict(orient="records")
    else:
        records = people

    for person in records:
        actual_name = str(person.get("Name", "")).strip()
        nickname = str(person.get("Nickname", "")).strip()

        if actual_name and (
            actual_name.casefold() == query
            or nickname.casefold() == query
        ):
            if actual_name not in candidates:
                candidates.append(actual_name)

    if len(candidates) == 1:
        return candidates[0], candidates

    return None, candidates


# FIX: Convert Gemini month text into a numeric month.
def normalize_month(month):
    if month is None:
        return None

    value = str(month).strip().casefold()

    for number in range(1, 13):
        if value in (
            calendar.month_name[number].casefold(),
            calendar.month_abbr[number].casefold(),
            str(number),
        ):
            return number

    return None

def normalize_relationship(relationship, people):
    if relationship is None:
        return None

    value = str(relationship).strip().casefold()

    # Match the original relationship spelling in Excel.
    if hasattr(people, "columns") and "Relationship" in people.columns:
        for item in people["Relationship"].dropna().unique():
            if str(item).strip().casefold() == value:
                return str(item).strip()

    return value.title()
def understand_message_with_llm(message, people):
    """
    Use Gemini for intent and entity extraction.
    Fall back to V3 deterministic NLU if Gemini fails.
    """

    fallback = understand_message(message, people)

    if not GEMINI_API_KEY:
        return fallback

    try:
        client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options={
                "timeout": 12000,
                "retry_options": {
                    "attempts": 1
                },
            },
        )

        prompt = f"""
You are an NLU component for a birthday assistant.

Your ONLY task is to understand the user's message.

Allowed intents:
- greeting
- help
- place_lookup
- age_lookup
- birthday_count
- upcoming_birthdays
- birthday_lookup
- unknown

Extract these entities when present:
- person_name
- relationship
- month
- place

Rules:
1. Do not answer the user's question.
2. Do not invent names, dates, or birthdays.
3. Use null for entities that are not present.
4. Return unknown for unsupported requests.
5. Interpret natural language and spelling variations.
6. Return only the structured information.

User message: {message}
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": RESPONSE_SCHEMA,
                "temperature": 0,
            },
        )

        if not response.text:
            return fallback

        result = json.loads(response.text)

        # Handle JSON returned as a string.
        if isinstance(result, str):
            result = json.loads(result)

        if not isinstance(result, dict):
            return fallback

        intent = result.get("intent")
        entities = result.get("entities", {})

        # Handle entities returned as a JSON string.
        if isinstance(entities, str):
            entities = json.loads(entities)

        if intent not in ALLOWED_INTENTS:
            return fallback

        if not isinstance(entities, dict):
            return fallback

        raw_name = entities.get("person_name")

        # Validate the person against the Excel dataset.
        person_name, person_candidates = normalize_person_name(
            raw_name, people
        )

        return {
            "intent": intent,
            "entities": {
                "person_name": person_name,
                "person_candidates": person_candidates,
                "relationship": normalize_relationship(
    entities.get("relationship"), people
),
                # FIX: Convert month name to number (September -> 9).
                "month": normalize_month(entities.get("month")),
                "place": entities.get("place"),
            },
        }

    except Exception as error:
        print(f"Gemini NLU fallback: {error}")
        traceback.print_exc()
        return fallback
