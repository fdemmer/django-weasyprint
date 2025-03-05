all: _list

test:
	tox --parallel auto --recreate

clean:
	rm -rf build dist
	rm -rf *.egg-info

build:
	python -m build

publish-test: clean build
	python -m twine upload -r testpypi dist/*

publish: clean build
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		python -m twine upload -r django-weasyprint dist/*; \
	else \
		echo Aborting upload: working directory is dirty >&2; \
	fi;


# list all targets (https://stackoverflow.com/a/26339924/652457)
.PHONY: _list
_list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs
