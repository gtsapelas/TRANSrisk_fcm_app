web: python manage.py migrate
web: python manage.py collectstatic --noinput
web: gunicorn TRANSrisk_fcm_project.wsgi --log-file -