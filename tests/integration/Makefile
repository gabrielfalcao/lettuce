all: django

export PYTHONPATH:=  ${PWD}/../../

django:
	@echo "running lettuce against a django project (harvest)"
	@cd alfaces && python manage.py harvest --verbosity=3
