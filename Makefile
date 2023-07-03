run:
	python3 manage.py runserver
cel:
	celery -A core worker -l INFO
