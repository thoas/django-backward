pep8:
	flake8 backward --ignore=E501,E127,E128,E124

test:
	coverage run --branch --source=backward manage.py test backward
	coverage report --omit=backward/test*

release:
	python setup.py sdist register upload -s
