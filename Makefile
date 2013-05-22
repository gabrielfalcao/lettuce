all: check_dependencies unit functional integration doctest

filename=lettuce-`python -c 'import lettuce;print lettuce.version'`.tar.gz

export PYTHONPATH:= ${PWD}
export LETTUCE_DEPENDENCIES:= nose mox sphinx lxml django fuzzywuzzy mock

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@for dependency in `echo $$LETTUCE_DEPENDENCIES`; do \
		python -c "import $$dependency" 2>/dev/null || (echo "You must install $$dependency in order to run lettuce's tests" && exit 3) ; \
		done

unit: clean
	@echo "Running unit tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/unit --cover-package=lettuce

functional: clean
	@echo "Running functional tests ..."
	@nosetests --stop -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/functional --cover-package=lettuce

integration: clean
	@echo "Running integration tests ..."
	@nosetests --stop -s --verbosity=2 tests/integration

doctest: clean
	@find specs -name '*.md' -exec steadymark {} \;

documentation:
	@markment --theme=flat-ui -o ./_public specs

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -delete; done
	@echo "OK!"

withdraw-documentation:
	@printf 'Removing current documentation ...'
	@ssh gabrielfalcao@gabrielfalcao.com rm -rf lettuce.it/public/*
	@echo "DONE!"

deploy-documentation:documentation withdraw-documentation
	@printf 'Deploying documentation to http://lettuce.it ...'
	@cd ./_public && tar -zcp *  | ssh gabrielfalcao@gabrielfalcao.com "tar zxp -C ./lettuce.it/public/"
	@echo "DONE!"

deploy: deploy-documentation

release: clean unit functional integration doctest deploy-documentation publish
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) lettuce setup.py README.md COPYING
	@echo "DONE!"

publish:
	@python setup.py sdist register upload
