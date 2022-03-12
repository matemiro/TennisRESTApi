release: python3 manage.py makemigrations
release: python3 manage.py migrate
release: python3 manage.py test players_profile.tests
web gunicorn tennis_api.wsgi --log-file -