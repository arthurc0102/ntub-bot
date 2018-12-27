# Application definition

ADMIN_APPS = [
    'jet',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'bootstrap4',
]

LOCAL_APPS = [
    'app.assessments',
    'app.common',
]

INSTALLED_APPS = ADMIN_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
