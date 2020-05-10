# Settings for use in production.

from django_heroku import settings as heroku_settings

print('Using production settings.')


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


heroku_settings(locals())
