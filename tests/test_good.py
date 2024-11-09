"""
test_good.py - contains all valid test cases
"""

import secrets
import statistics

from sanic import Sanic
from pytest import approx
from tinydb import where, TinyDB
from sanic_testing.testing import SanicTestClient

from tests.payload import make_payload, make_payload_raw


def test_successful_insight(app: Sanic) -> None:
    test_client: SanicTestClient = app.test_client
    survey_results = [7, 7, 4, 1, 6, 6, 2, 7, 6, 6]

    req, resp = test_client.post("/process-survey", json=make_payload(survey_results=survey_results))

    insights = resp.json

    assert resp.status == 200

    assert insights["cat_dog"] == "dogs"
    assert insights["fur_value"] == "long"
    assert insights["tail_value"] == "short"
    assert insights["overall_analysis"] == "unsure"


def test_database_update(app: Sanic, db: TinyDB) -> None:
    test_client: SanicTestClient = app.test_client
    rand_user_id = f"test_user_{secrets.token_urlsafe(8)}"

    count_before = len(db)

    req, resp = test_client.post("/process-survey", json=make_payload_raw(rand_user_id))

    count_after = len(db)

    assert resp.status == 200
    assert count_after > count_before

    assert db.contains(where("user_id") == rand_user_id)  # noqa


def test_certain_cat_insight(app: Sanic) -> None:
    test_client: SanicTestClient = app.test_client
    survey_results = [2, 7, 7, 4, 1, 1, 6, 6, 4, 7]

    req, resp = test_client.post("/process-survey", json=make_payload(survey_results=survey_results))

    insights = resp.json

    assert resp.status == 200

    assert insights["cat_dog"] == "cats"
    assert insights["fur_value"] == "short"
    assert insights["tail_value"] == "long"
    assert insights["overall_analysis"] == "certain"


def test_statistic_update(app: Sanic, db: TinyDB) -> None:
    payload = make_payload()
    test_client: SanicTestClient = app.test_client

    values = [result["question_value"] for result in payload["survey_results"]]

    mean = statistics.mean(values)
    median = statistics.median(values)
    std_dev = statistics.stdev(values)

    req, resp = test_client.post("/process-survey", json=payload)

    assert resp.status == 200

    doc = db.get(where("user_id") == payload["user_id"])  # noqa

    assert doc is not None
    assert doc["mean"] == approx(mean)
    assert doc["median"] == approx(median)
    assert doc["std_dev"] == approx(std_dev)
