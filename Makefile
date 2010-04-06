all: unit functional doctests

unit:
	@echo "Running unit tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/unit/ --cover-package=lettuce

functional:
	@echo "Running functional tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/functional/ --cover-package=lettuce

doctests:
	@echo "Running doctests..."
	@find docs -name '*.rst' -exec printf "    on file "{}" ..." \; -exec python -c "import doctest;doctest.testfile('{}', verbose=False, report=True)" \; -exec echo " ok" \; 
	@echo "tests passed!"

clean:
	@echo -n "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"
