all: check_dependencies unit functional doctest

filename=lettuce-`python -c 'import lettuce;print lettuce.version'`.tar.bz2

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@python -c 'import mox' 2>/dev/null || echo 'You must install mox to run tests'
	@python -c 'import mox' 2>/dev/null || exit 3
	@python -c 'import sphinx' 2>/dev/null || echo 'You must install sphinx to run tests'
	@python -c 'import sphinx' 2>/dev/null || exit 3
	
unit: clean
	@echo "Running unit tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/unit/ --cover-package=lettuce

functional: clean
	@echo "Running functional tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/functional/ --cover-package=lettuce

doctest: clean
	@cd docs && make doctest

documentation:
	@cd docs && make html

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

withdraw-documentation:
	@printf 'Removing current documentation ...'
	@ssh gabrielfalcao@gabrielfalcao.com rm -rf lettuce.it/public/*
	@echo "DONE!"

deploy-documentation:documentation withdraw-documentation
	@printf 'Deploying documentation to http://lettuce.it ...'
	@cd ./docs/_build/html && tar -zcp *  | ssh gabrielfalcao@gabrielfalcao.com "tar zxp -C ./lettuce.it/public/"
	@echo "DONE!"

deploy: deploy-documentation

release: clean
	@printf "Exporting to $(filename)... "
	@git archive HEAD | bzip2 > $(filename)
	@echo "DONE!"
