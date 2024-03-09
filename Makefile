#VERSION=$(shell cd backend && poetry run python -c 'import nebula' --version)

check:
	poetry run ruff format . && \
	poetry run ruff check --fix . && \
	poetry run mypy .

#check_version:
#	cd backend && poetry version $(VERSION)
