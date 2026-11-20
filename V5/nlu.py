
import re
import calendar

MONTHS = {
    name.lower(): number
    for number, name in enumerate(calendar.month_name)
    if name
}

RELATIONSHIP_ALIASES = {
    "wife": "Wife",
    "spouse": "Wife",
    "father": "Father",
    "dad": "Father",
    "appa": "Father",
    "mother": "Mother",
    "mom": "Mother",
    "amma": "Mother",
    "brother": "Brother",
    "brothers": "Brother",
    "sister": "Sister",
    "sisters": "Sister",
    "nephew": "Nephew",
    "niece": "Niece",
    "uncle": "Uncle",
    "aunt": "Aunt",
    "cousin": "Cousin",
    "friend": "Friend",
    "colleague": "Colleague",
    "student": "Student",
    "neighbour": "Neighbour",
    "neighbor": "Neighbour"
}


def contains_phrase(text, phrase):
    return re.search(
        r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)",
        text.lower()
    ) is not None


def recognize_intent(text):
    text = text.lower().strip()

    if not text:
        return "unknown"

    if text in ["hi", "hello", "hey", "good morning", "good evening"]:
        return "greeting"

    if any(word in text for word in ["help", "examples", "what can i ask"]):
        return "help"

    if any(word in text for word in ["where", "stay", "lives", "live"]):
        return "place_lookup"

    if any(word in text for word in ["how old", "age"]):
        return "age_lookup"

    if any(word in text for word in ["how many", "count", "number of"]):
        return "birthday_count"

    if any(word in text for word in [
        "upcoming", "tomorrow", "today", "next 7 days",
        "next week", "this week", "coming birthdays"
    ]):
        return "upcoming_birthdays"

    if "birthday" in text or "birthdays" in text:
        return "birthday_lookup"

    if "when is" in text or "when's" in text:
        return "birthday_lookup"

    return "unknown"


def extract_entities(text, people=None):
    text = text.lower().strip()

    entities = {
        "person_name": None,
        "person_candidates": [],
        "relationship": None,
        "month": None,
        "place": None
    }

    # Match full names and nicknames from the dataset.
    if people is not None:
        full_name_matches = []
        nickname_matches = []

        for _, person in people.iterrows():
            name = str(person["Name"]).strip()
            nickname = str(person["Nickname"]).strip()

            if name and name.lower() != "nan":
                if contains_phrase(text, name):
                    full_name_matches.append(name)

            if (
                nickname
                and nickname.lower() != "nan"
                and len(nickname) >= 3
                and contains_phrase(text, nickname)
            ):
                nickname_matches.append(name)

        # Exact full names take priority over nicknames.
        if full_name_matches:
            entities["person_candidates"] = list(
                dict.fromkeys(full_name_matches)
            )
        else:
            entities["person_candidates"] = list(
                dict.fromkeys(nickname_matches)
            )

        # Set person_name only when there is one unambiguous match.
        if len(entities["person_candidates"]) == 1:
            entities["person_name"] = entities["person_candidates"][0]

    # Extract relationship.
    for alias in sorted(RELATIONSHIP_ALIASES, key=len, reverse=True):
        if contains_phrase(text, alias):
            entities["relationship"] = RELATIONSHIP_ALIASES[alias]
            break

    # Extract month.
    for month, number in MONTHS.items():
        if contains_phrase(text, month):
            entities["month"] = number
            break

    # Extract place.
    if people is not None:
        for place in sorted(
            people["Place_of_Stay"].dropna().unique(),
            key=len,
            reverse=True
        ):
            if place and contains_phrase(text, str(place)):
                entities["place"] = str(place)
                break

    return entities


def understand_message(text, people=None):
    intent = recognize_intent(text)
    entities = extract_entities(text, people)

    return {
        "intent": intent,
        "entities": entities
    }
