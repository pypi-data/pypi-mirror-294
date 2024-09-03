version := `uv run python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])'`


default: dev

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache build dist *.egg-info

sync:
    uv sync

build: clean lint audit test
    uvx --from build pyproject-build --installer uv

format:
    uv run ruff check --select I --fix src app tests
    uv run ruff format src app tests

lint: format
    uv run ruff check src app tests
    uv run mypy src app

audit:
    uv run pip-audit
    uv run bandit -r -c "pyproject.toml" src

test:
    uv run pytest tests

publish: build cookiecutter
    uvx twine upload dist/**
    git tag -a 'v{{version}}' -m 'v{{version}}'
    git push origin v{{version}}

cookiecutter:
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}
    cp -R demo cookiecutter/{{{{cookiecutter.project_slug}}
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.idea
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.mypy_cache
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.pytest_cache
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.ruff_cache
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.venv
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/app.egg-info
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/build
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/dist
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/tmp
    rm -rf cookiecutter/{{{{cookiecutter.project_slug}}/.env

    cp cookiecutter/templates/.env cookiecutter/{{{{cookiecutter.project_slug}}
    cp cookiecutter/templates/README.md cookiecutter/{{{{cookiecutter.project_slug}}
    cp cookiecutter/templates/hosts.yml cookiecutter/{{{{cookiecutter.project_slug}}/ansible/hosts.yml

    mkdir cookiecutter/{{{{cookiecutter.project_slug}}/tmp
    touch cookiecutter/{{{{cookiecutter.project_slug}}/tmp/todo.txt
    touch cookiecutter/{{{{cookiecutter.project_slug}}/tmp/tmp.py


dev:
    uv run uvicorn --reload --port 3000 --log-level warning app.main:server
