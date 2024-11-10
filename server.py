import os
import sys
import pathlib

from sanic import Sanic
from sanic.request import Request
from sanic_ext import validate, Extend
from sanic.response import json, JSONResponse

from tinydb import where
from aiotinydb import AIOTinyDB

from models import Payload, Insights, Statistics, StatisticsQuery


BASE_DIR = pathlib.Path(__file__).parent

if any("test" in arg for arg in sys.argv):
    DB_PATH = BASE_DIR / "db_test.json"
else:
    DB_PATH = BASE_DIR / "db.json"  # pragma: no cover


def create_app() -> Sanic:
    app = Sanic("educhamp")

    app.config.CORS_ORIGINS = ["http://localhost:5173"]
    Extend(app)

    if "COVERAGE_RUN" in os.environ:
        # Sanic generates source code on the fly. This is a workaround to make sure coverage.py
        # can track the generated source code. See https://github.com/sanic-org/sanic/issues/2702
        app.config.TOUCHUP = False

    @app.signal("survey.secondary_analysis.generate")
    async def secondary_analysis(**context):
        doc_id = context["doc_id"]
        async with AIOTinyDB(DB_PATH) as db:
            statistics = Statistics.from_payload(context["payload"])
            db.update(statistics.model_dump(), doc_ids=[doc_id])

    @app.post("/process-survey")
    @validate(json=Payload)
    async def process_survey(request: Request, body: Payload) -> JSONResponse:
        insights = await Insights.from_payload(body)
        insight_json = insights.model_dump()

        async with AIOTinyDB(DB_PATH) as db:
            doc_id = db.insert(insight_json | {"user_id": body.user_id})
            context = {"doc_id": doc_id, "payload": body}
            await request.app.dispatch("survey.secondary_analysis.generate", context=context)

        return json(insight_json)

    @app.route("/stats")
    @validate(query=StatisticsQuery)
    async def stats(request: Request, query: StatisticsQuery) -> JSONResponse:
        async with AIOTinyDB(DB_PATH) as db:
            doc = db.get(where("user_id") == query.user_id)  # noqa
            if doc is None:
                return json({"message": "User not found"}, status=404)
            return json({"mean": doc["mean"], "median": doc["median"], "std_dev": doc["std_dev"]})

    return app


if __name__ == "__main__":
    server = create_app()
    server.run(debug=True)
