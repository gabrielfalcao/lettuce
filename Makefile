all: unit functional doctest

unit:
	@echo "Running unit tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/unit/ --cover-package=lettuce

functional:
	@echo "Running functional tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/functional/ --cover-package=lettuce

doctest:
	@cd docs && make doctest

documentation:
	@cd docs && make html

clean:
	@echo -n "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"


deploy-documentation: documentation
	@printf 'Removing current documentation ...'
	@ssh gabrielfalcao@gabrielfalcao.com rm -rf lettuce.it/public/*
	@echo "DONE!"
	@printf 'Deploying documentation to http://lettuce.it ...'
	@cd ./docs/_build/html && tar -zcp *  | ssh gabrielfalcao@gabrielfalcao.com "tar zxp -C ./lettuce.it/public/"
	@echo "DONE!"

deploy: deploy-documentation

