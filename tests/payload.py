import random
import secrets
from typing import Optional, List, Dict, Tuple


def make_payload(user_id: Optional[str] = None, survey_results: List[int] = None) -> Dict:
    if survey_results is None:
        survey_results = [random.randint(1, 7) for _ in range(10)]

    return make_payload_raw(user_id, [(qnum + 1, qval) for qnum, qval in enumerate(survey_results)])


def make_payload_raw(user_id: Optional[str] = None, survey_results: List[Tuple[int, int]] = None) -> Dict:
    """
    Pretty much the same as make_payload but with a different format for survey_results.
    Need this to mock the payload for the test cases where the input data is invalid (aka
    the question numbers are not unique or the length is not 10).
    """

    if user_id is None:
        user_id = f"test_user_{secrets.token_urlsafe(8)}"

    if survey_results is None:
        survey_results = [(qnum + 1, random.randint(1, 7)) for qnum in range(10)]

    return {
        "user_id": user_id,
        "survey_results": [{"question_number": qnum, "question_value": qval} for qnum, qval in survey_results],
    }
