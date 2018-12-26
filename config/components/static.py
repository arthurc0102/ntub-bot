from config.settings import root


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    root('static'),
]

STATIC_ROOT = root('assets')

MEDIA_URL = '/media/'

MEDIA_ROOT = root('media')
