install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	pip install --user ~/Desktop/hexlet_projects/python-project-lvl2/dist/*.whl
package-reinstall:
	pip install --user ~/Desktop/hexlet_projects/python-project-lvl2/dist/*.whl --force-reinstall
page_loader:
	poetry run page_loader
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml
