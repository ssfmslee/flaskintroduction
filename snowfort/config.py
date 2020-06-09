import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'ldpeicxZYzgUwA_OJJRsGqF-cdz0OgDbJWeOb9N6QxQ='

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'development.db')
#SQLALCHEMY_DATABASE_URI = 'mysql://root:stanfords3l@localhost/snowfort'
SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/snowfort'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'GDqXwlp10op8FQCVIE5OONuL5U208qJgWhKegIrBA_A='
