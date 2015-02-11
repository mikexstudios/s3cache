FROM python:2.7-onbuild
EXPOSE 8000
CMD gunicorn --config gunicorn.py.ini app:app
