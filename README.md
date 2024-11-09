# Educhamp Assignment

[![Educhamp](https://github.com/mentix02/educhamp/actions/workflows/python-app.yml/badge.svg)](https://github.com/mentix02/educhamp/actions/workflows/python-app.yml)

Simple breakdown of the codebase:

1. [`server.py`](server.py) - Contains the main server code with the API endpoints.
2. [`models.py`](models.py) - Contains the Pydantic models for the API.
3. [`description.py`](description.py) - Methods to call OpenAI to generate descriptions.
4. [`tests/payload.py`](tests/payload.py) - Methods to mock the payload for the tests.
5. [`tests/test_bad.py`](tests/test_bad.py) - Tests sending invalid payloads.
6. [`tests/test_good.py`](tests/test_good.py) - Tests sending valid payloads.
7. [`tests/conftest.py`](tests/conftest.py) - Contains pytest fixtures.

## Getting Started

Make sure to have Python 3.9+ installed on your system.

```shell
# Clone the repository
git clone git@github.com:mentix02/educhamp.git && cd educhamp
# Install dependencies (preferably in a virtual environment)
pip install -r requirements.txt
# Run the server
sanic "server:create_app"
```

## Testing

We use [pytest](https://docs.pytest.org/en/stable/). To run the tests, use the following command (sets up the PYTHONPATH for you):

```shell
# Run the tests
make test
```

## Coverage

We use [coverage.py](https://coverage.readthedocs.io/en/7.6.4/).

```shell
# Run the tests with coverage
make html
```

Open `htmlcov/index.html` in your browser to view the coverage report.
