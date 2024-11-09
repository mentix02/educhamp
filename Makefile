.PHONY: test

test:
	PYTHONPATH=. pytest

coverage:
	PYTHONPATH=. coverage run -m pytest

html: coverage
	coverage html

clean:
	rm -rf htmlcov __pycache__ .coverage db_test.json
