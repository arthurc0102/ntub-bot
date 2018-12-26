from config.components.app import INSTALLED_APPS


DEVELOPING_APPS = [
    'django_extensions',
]

INSTALLED_APPS.extend(DEVELOPING_APPS)
