"""
test_bad.py - contains all invalid test cases
"""

from sanic import Sanic
from tinydb import TinyDB
from sanic_testing.testing import SanicTestClient

from tests.payload import make_payload, make_payload_raw


def test_duplicate_question_numbers(app: Sanic, db: TinyDB) -> None:
    """
    Duplicate question numbers sent.
    """

    test_client: SanicTestClient = app.test_client
    survey_results = [(1, 7), (1, 7), (4, 4), (1, 1), (6, 6), (6, 6), (2, 2), (7, 7), (6, 6), (6, 6)]

    before_count = len(db)

    req, resp = test_client.post("/process-survey", json=make_payload_raw(survey_results=survey_results))

    after_count = len(db)

    assert resp.status == 400
    assert before_count == after_count


def test_incomplete_survey(app: Sanic, db: TinyDB) -> None:
    """
    Only 9 questions sent.
    """

    test_client: SanicTestClient = app.test_client
    survey_results = [(1, 7), (2, 7), (4, 4), (1, 1), (6, 6), (6, 6), (2, 2), (7, 7), (6, 6)]

    before_count = len(db)

    req, resp = test_client.post("/process-survey", json=make_payload_raw(survey_results=survey_results))

    after_count = len(db)

    assert resp.status == 400
    assert before_count == after_count


def test_invalid_question_numbers(app: Sanic, db: TinyDB) -> None:
    """
    Invalid question numbers sent.
    """

    test_client: SanicTestClient = app.test_client
    survey_results = [(1, 7), (2, 7), (-2, 4), (1, 1), (6, 6), (6, 6), (2, 2), (7, 7), (6, 6), (10, 10)]

    before_count = len(db)

    req, resp = test_client.post("/process-survey", json=make_payload_raw(survey_results=survey_results))

    after_count = len(db)

    assert resp.status == 400
    assert before_count == after_count


def test_invalid_question_values(app: Sanic, db: TinyDB) -> None:
    """
    Invalid question values sent.
    """

    test_client: SanicTestClient = app.test_client
    survey_results = [8, -9, 3, 11, 5, 6, 7, 8, 9, 10]

    before_count = len(db)

    req, resp = test_client.post("/process-survey", json=make_payload(survey_results=survey_results))

    after_count = len(db)

    assert resp.status == 400
    assert before_count == after_count


def test_fetch_invalid_stats(app: Sanic, db: TinyDB) -> None:
    test_client: SanicTestClient = app.test_client

    _, resp = test_client.get("/stats", params={"user_id": "does_not_exist"})
    assert resp.status == 404
