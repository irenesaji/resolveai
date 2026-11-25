
import pytest

import app.services.ticket_analyzer as analyzer


def test_valid_ticket_analysis(monkeypatch):
    fake_response = """
    {
        "category": "Billing",
        "sentiment": "Negative",
        "priority": "High",
        "suggested_response": "We are sorry. Please share your order ID."
    }
    """

    monkeypatch.setattr(
        analyzer,
        "generate_ai_response",
        lambda prompt: fake_response
    )

    result = analyzer.analyze_ticket("I was charged twice.")

    assert result["category"] == "Billing"
    assert result["sentiment"] == "Negative"
    assert result["priority"] == "High"
    assert isinstance(result["suggested_response"], str)


def test_invalid_json_response(monkeypatch):
    monkeypatch.setattr(
        analyzer,
        "generate_ai_response",
        lambda prompt: "This is not valid JSON"
    )

    with pytest.raises(ValueError):
        analyzer.analyze_ticket("My payment failed.")


def test_missing_analysis_field(monkeypatch):
    fake_response = """
    {
        "category": "Billing",
        "sentiment": "Negative",
        "priority": "High"
    }
    """

    monkeypatch.setattr(
        analyzer,
        "generate_ai_response",
        lambda prompt: fake_response
    )

    with pytest.raises(ValueError, match="Missing analysis field"):
        analyzer.analyze_ticket("I was charged twice.")


def test_invalid_sentiment(monkeypatch):
    fake_response = """
    {
        "category": "Billing",
        "sentiment": "Angry",
        "priority": "High",
        "suggested_response": "Please contact support."
    }
    """

    monkeypatch.setattr(
        analyzer,
        "generate_ai_response",
        lambda prompt: fake_response
    )

    with pytest.raises(ValueError, match="Invalid sentiment"):
        analyzer.analyze_ticket("My payment failed.")


def test_invalid_priority(monkeypatch):
    fake_response = """
    {
        "category": "Billing",
        "sentiment": "Negative",
        "priority": "Urgent",
        "suggested_response": "Please contact support."
    }
    """

    monkeypatch.setattr(
        analyzer,
        "generate_ai_response",
        lambda prompt: fake_response
    )

    with pytest.raises(ValueError, match="Invalid priority"):
        analyzer.analyze_ticket("My payment failed.")


def test_knowledge_context_is_included(monkeypatch):
    captured_prompt = {}

    def fake_response(prompt):
        captured_prompt["value"] = prompt

        return """
        {
            "category": "Refund",
            "sentiment": "Negative",
            "priority": "Medium",
            "suggested_response": "We will check your refund."
        }
        """

    monkeypatch.setattr(
        analyzer,
        "generate_ai_response",
        fake_response
    )

    analyzer.analyze_ticket(
        "Where is my refund?",
        "Refunds must be verified before approval."
    )

    assert (
        "Refunds must be verified before approval."
        in captured_prompt["value"]
    )


def test_invalid_category(monkeypatch):
    fake_response = """
    {
        "category": "Complaint",
        "sentiment": "Negative",
        "priority": "High",
        "suggested_response": "Please contact support."
    }
    """

    monkeypatch.setattr(
        analyzer,
        "generate_ai_response",
        lambda prompt: fake_response
    )

    with pytest.raises(ValueError, match="Invalid category"):
        analyzer.analyze_ticket("My payment failed.")
