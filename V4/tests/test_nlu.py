
from data_service import load_people
from nlu import understand_message, recognize_intent

PEOPLE = load_people()


def test_greeting_intent():
    assert recognize_intent("Hello") == "greeting"


def test_birthday_lookup_intent():
    assert recognize_intent(
        "When is Rahul Patil's birthday?"
    ) == "birthday_lookup"


def test_birthday_count_intent():
    assert recognize_intent(
        "How many birthdays are in September?"
    ) == "birthday_count"


def test_upcoming_birthday_intent():
    assert recognize_intent(
        "Who has birthdays tomorrow?"
    ) == "upcoming_birthdays"


def test_relationship_entity():
    result = understand_message(
        "When is my mother's birthday?", PEOPLE
    )
    assert result["entities"]["relationship"] == "Mother"


def test_month_entity():
    result = understand_message(
        "How many birthdays are in September?", PEOPLE
    )
    assert result["entities"]["month"] == 9


def test_person_entity():
    result = understand_message(
        "When is Rahul Patil's birthday?", PEOPLE
    )
    assert result["entities"]["person_name"] == "Rahul Patil"
