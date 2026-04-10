[private]
default:
    @just --list --unsorted

gha-update:
    uvx gha-update

test:
    uvx --with tox-uv tox --parallel auto

clean:
    rm -rf build dist
    rm -rf *.egg-info

build:
    python -m build

publish-test: clean build
    python -m twine upload -r testpypi dist/*

publish: clean build
    #!/usr/bin/env bash
    status=$(git status --porcelain)
    if [ -z "$status" ]; then
        python -m twine upload -r django-weasyprint dist/*
    else
        echo "Aborting upload: working directory is dirty" >&2
        exit 1
    fi
