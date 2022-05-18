from django.apps import AppConfig


class BusetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buset'
    INSTALLED_APPS = [
    'buset.apps.BusetConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
