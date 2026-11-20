
import pandas as pd

from dialogue import DialogueManager
from service import process_message


def sample_people():
    return pd.DataFrame([
        {
            "Person_ID": 1,
            "Name": "Rahul Sharma",
            "Nickname": "Rahu",
            "DOB": pd.Timestamp("2002-09-15"),
            "Place_of_Stay": "Bengaluru",
            "Relationship": "Friend",
            "Relationship_Group": "Personal",
            "Relationship_Detail": "Friend"
        },
        {
            "Person_ID": 2,
            "Name": "Ravi Kumar",
            "Nickname": "Rahu",
            "DOB": pd.Timestamp("2001-10-20"),
            "Place_of_Stay": "Mysuru",
            "Relationship": "Friend",
            "Relationship_Group": "Personal",
            "Relationship_Detail": "Friend"
        },
        {
            "Person_ID": 3,
            "Name": "Anil Kumar",
            "Nickname": "Anil",
            "DOB": pd.Timestamp("2000-09-10"),
            "Place_of_Stay": "Bengaluru",
            "Relationship": "Nephew",
            "Relationship_Group": "Family",
            "Relationship_Detail": "Nephew"
        }
    ])


def test_dialogue_manager_reset():
    manager = DialogueManager()

    manager.update_context(
        intent="birthday_count",
        entities={"month": 9, "relationship": "Nephew"}
    )

    manager.reset()

    assert manager.get_context()["month"] is None
    assert manager.get_context()["relationship"] is None
    assert manager.get_context()["last_intent"] is None


def test_month_follow_up():
    people = sample_people()

    first = process_message(
        people,
        "How many birthdays are in September?"
    )

    second = process_message(
        people,
        "What about October?",
        context=first["context"]
    )

    assert "September" in first["answer"]
    assert "October" in second["answer"]
    assert second["context"]["month"] == 10


def test_relationship_context_follow_up():
    people = sample_people()

    first = process_message(
        people,
        "Any nephew birthdays in September?"
    )

    second = process_message(
        people,
        "What about October?",
        context=first["context"]
    )

    assert second["context"]["relationship"] == "Nephew"
    assert "Nephew" in second["answer"]


def test_ambiguous_nickname_clarification():
    people = sample_people()

    result = process_message(
        people,
        "When is Rahu's birthday?"
    )

    assert "multiple people" in result["answer"].lower()
    assert result["context"]["pending_clarification"] is not None


def test_clarification_resolution():
    people = sample_people()

    first = process_message(
        people,
        "When is Rahu's birthday?"
    )

    second = process_message(
        people,
        "Rahul Sharma",
        context=first["context"]
    )

    assert "Rahul Sharma" in second["answer"]
    assert second["context"]["pending_clarification"] is None


def test_reset_context_object():
    manager = DialogueManager({
        "last_intent": "birthday_count",
        "month": 9,
        "relationship": "Nephew"
    })

    manager.reset()

    assert manager.get_context()["month"] is None
    assert manager.get_context()["relationship"] is None
