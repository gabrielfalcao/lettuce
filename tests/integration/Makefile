all: django

export PYTHONPATH:=  ${PWD}/../../

django:
	@echo $$PYTHONPATH
	@echo "running lettuce against a django project (harvest)"
	@cd alfaces && python manage.py harvest
