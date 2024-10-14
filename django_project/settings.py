import os
import sys
from pathlib import Path
from celery.schedules import crontab
import environ
from django.contrib.messages import constants as messages

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# False if not in os.environ
# DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
# SECRET_KEY = env('SECRET_KEY')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG']
# DEBUG = False # enable for production

ALLOWED_HOSTS = [".replit.dev", ".replit.app"]
CSRF_TRUSTED_ORIGINS = ["https://*.replit.dev", "https://*.replit.app"]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     'debug_toolbar',
]

CUSTOM_APPS = ['core.apps.CoreConfig']

THIRD_PARTY_APPS = ['crispy_forms', 'crispy_bootstrap5']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

AUTH_USER_MODEL = 'core.User'

AUTHENTICATION_BACKENDS = [
    # 'django.contrib.auth.backends.ModelBackend',
    'core.backends.EmailBackend',
]



CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'core:login'
LOGOUT_REDIRECT_URL = 'core:login'
HOME_REDIRECT_URL = '/'

SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGING = (
    60 * 60 * 24 * 14
)  # Session will be expired in 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = (
    False  # Do not expire session when browser is closed
)
# messages customization settings
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
    messages.INFO: 'info',
    messages.WARNING: 'warning',
}

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    # Custom Middleware
    'core.middleware.RedirectAuthenticatedUserMiddleware',
    'core.middleware.UrlNotFoundInterceptionMiddleware',
]


if DEBUG is False:
    del MIDDLEWARE[0]

# Only use clickjacking protection in deployments because the Development Web View uses
# iframes and needs to be a cross origin.
if "REPLIT_DEPLOYMENT" in os.environ:
    MIDDLEWARE.append('django.middleware.clickjacking.XFrameOptionsMiddleware')

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                # 'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'django_project/static',
]
MEDIA_URL = '/media/'
STATIC_ROOT = 'media'

INTERNAL_IPS = [
    '127.0.0.1',  # For localhost access
    '2f8112c9-cb1b-440c-ae1b-6e29351a4060-00-dbccepdzye9t.picard.replit.dev'  # Replit public URL
]



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Deployment settings and configurations
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ['FROM_DEFAULT_EMAIL']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False

    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_DIRECT_EXEPT = []
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = False
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARED_PROTO', 'https')
    SECURE_SSL_HOST = True
    
    CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['POSTGRES_DATABASE_NAME'],
            'USER': os.environ['POSTGRES_DATABASE_USERNAME'],
            'PASSWORD': os.environ['POSTGRES_DATABASE_PASSWORD'],
            'HOST': os.environ['POSTGRES_DATABASE_HOSTNAME'],
            'PORT': os.environ['POSTGRES_DATABASE_PORT'],
        }
    }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Celery tasks & workers settings
CELERY_BROKER_URL = 'redis://https://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
   'run_tests_monthly':{
       'task': 'core.tasks.run_tests',
       'schedule': crontab(day_of_month=str(1), hour=str(0), minute=str(0))
   },
}
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True
# CELERY_TASK_DEFAULT_QUEUE = 'default'
# CELERY_TASK_DEFAULT_EXCHANGE = 'default'
# CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'
# CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
# CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'
# CELERY_TASK_DEFAULT_QUEUE = 'default'
# CELERY_TASK_DEFAULT_EXCHANGE = 'default'

FROM_DEFAULT_EMAIL = os.environ['FROM_DEFAULT_EMAIL']
# X_FRAME_OPTIONS = 'ALLOW-FROM https://2f8112c9-cb1b-440c-ae1b-6e29351a4060-00-dbccepdzye9t.picard.replit.dev/'
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
GOOGLE_REDIRECT_URI = os.environ['GOOGLE_REDIRECT_URI']
GOOGLE_AUTHORIZATION_URL = os.environ['GOOGLE_AUTHORIZATION_URL']
GOOGLE_TOKEN_URL = os.environ['GOOGLE_TOKEN_URL']
GOOGLE_USERINFO_URL= os.environ['GOOGLE_USERINFO_URL']



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
