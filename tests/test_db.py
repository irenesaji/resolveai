
import database.db as db


def test_ticket_creation_and_retrieval(tmp_path, monkeypatch):
    test_db = tmp_path / "test_resolveai.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)

    db.initialize_database()

    db.create_ticket(
        "RES-TEST1001",
        "Test Customer",
        "test@example.com",
        "My order was not delivered."
    )

    ticket = db.get_ticket_by_id("RES-TEST1001")

    assert ticket is not None
    assert ticket[2] == "Test Customer"
    assert ticket[5] == "Unclassified"
    assert ticket[8] == "Open"


def test_ticket_analysis_update(tmp_path, monkeypatch):
    test_db = tmp_path / "test_analysis.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)

    db.initialize_database()

    db.create_ticket(
        "RES-TEST1002",
        "Test Customer",
        "test@example.com",
        "I need a refund."
    )

    db.update_ticket_analysis(
        "RES-TEST1002",
        "Refund",
        "Negative",
        "High",
        "We apologize for the inconvenience."
    )

    ticket = db.get_ticket_by_id("RES-TEST1002")

    assert ticket[5] == "Refund"
    assert ticket[6] == "Negative"
    assert ticket[7] == "High"
    assert ticket[9] == "We apologize for the inconvenience."


def test_response_review(tmp_path, monkeypatch):
    test_db = tmp_path / "test_review.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)

    db.initialize_database()

    db.create_ticket(
        "RES-TEST1003",
        "Test Customer",
        "test@example.com",
        "Please help me."
    )

    db.update_response_review(
        "RES-TEST1003",
        "Approved"
    )

    ticket = db.get_ticket_by_id("RES-TEST1003")

    assert ticket[11] == "Approved"


def test_ticket_status_update(tmp_path, monkeypatch):
    test_db = tmp_path / "test_status.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)

    db.initialize_database()

    db.create_ticket(
        "RES-TEST1004",
        "Test Customer",
        "test@example.com",
        "My issue is resolved."
    )

    db.update_ticket_status(
        "RES-TEST1004",
        "Resolved"
    )

    ticket = db.get_ticket_by_id("RES-TEST1004")

    assert ticket[8] == "Resolved"
