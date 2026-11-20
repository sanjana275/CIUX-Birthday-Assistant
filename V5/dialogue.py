
class DialogueManager:
    """
    Manages conversation context for Birthday Assistant V3.
    """

    def __init__(self, initial_context=None):
        self.reset()

        if isinstance(initial_context, dict):
            self.context.update(initial_context)

    def reset(self):
        """Clear all conversation context."""
        self.context = {
            "last_intent": None,
            "month": None,
            "relationship": None,
            "person_name": None,
            "pending_clarification": None
        }

    def update_context(self, intent=None, entities=None):
        """Store newly recognized information."""

        entities = entities or {}

        if intent and intent != "unknown":
            self.context["last_intent"] = intent

        for key in ["month", "relationship", "person_name"]:
            value = entities.get(key)

            if value is not None:
                self.context[key] = value

        return self.context

    def get_context(self):
        """Return the current conversation context."""
        return self.context

    def set_clarification(self, clarification):
        self.context["pending_clarification"] = clarification

    def clear_clarification(self):
        self.context["pending_clarification"] = None
