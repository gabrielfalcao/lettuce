all: unit functional

unit:
	@echo "Running unit tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-inclusive tests/unit/
functional:
	@echo "Running functional tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-inclusive tests/functional/

clean:
	@echo -n "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"
