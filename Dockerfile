FROM python:2.7-onbuild
EXPOSE 80
CMD gunicorn --config gunicorn.py.ini app:app