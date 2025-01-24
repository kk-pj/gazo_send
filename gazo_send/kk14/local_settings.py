DEBUG = True

ALLOWED_HOSTS = ['*']

try:
    from .local_settings import *
except:
    pass