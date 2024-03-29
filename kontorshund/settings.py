import os
import sys
from pathlib import Path
from urllib.parse import urljoin
from django.utils.log import DEFAULT_LOGGING
from django.contrib.messages import constants as messages

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import logging
logger = logging.getLogger('SETTINGS')


NUMBER_OF_ADS_OFFERED_AT_DISCOUNT = 50

PRICE_DURING_DISCOUNT = 10
PRICE_DURING_DISCOUNT_STRING = f'{PRICE_DURING_DISCOUNT} kr'

REGULAR_PRICE = 40
REGULAR_PRICE_STRING = f'{REGULAR_PRICE} kr'


# reCAPTCHA
RECAPTCHA_SITE_KEY = os.environ.get('reCAPTCHA_SITE_KEY') 
RECAPTCHA_SECRET_KEY = os.environ.get('reCAPCHA_SECRET_KEY') 

# Swish constants
NGROK_URL = "https://6054-92-33-202-136.ngrok.io" # Fill out with new value when testing 
SWISH_PAYEEALIAS = os.environ.get('MERCHANT_SWISH_NUMBER') # This would be your merchant swish number in production. In test it doesnt matter
SWISH_ROOTCA = "/home/dockeruser/web/Certificates_prod/Swish_TLS_RootCA.pem"
SWISH_CERT = ("/home/dockeruser/web/Certificates_prod/swish_certificate_202112151645.pem", "/home/dockeruser/web/Certificates_prod/private.key")
#SWISH_URL = "https://mss.cpc.getswish.net/swish-cpcapi/api/" # DEVELOPMENT
SWISH_URL = "https://cpc.getswish.net/swish-cpcapi/api/" # PRODUCTION

ALLOWED_NGROK = NGROK_URL[8:]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "ndkwjankgsa")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG'] == 'TRUE'

print(f'Debug is {DEBUG}')


ALLOWED_HOSTS = [
    'localhost', 
    '0.0.0.0', 
    'e40c-92-33-202-136.ngrok.io',

    'kontorshund.se',
    'www.kontorshund.se',

]

ALLOWED_HOSTS.append(ALLOWED_NGROK)

# Allowing Docker hosts as allowed hosts
ALLOWED_CIDR_NETS = ['172.16.0.0/12']

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [

    # All-auth
    'allauth', 
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # Django autocomplete light
    #"debug_toolbar",
    'dal',
    'dal_select2',

    # Django-Default
    'django_admin_env_notice',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django-added
    'django.contrib.sites',

    # Other third-party
    'crispy_forms',
    'django_extensions',
    'lockdown',
    'storages',
    'stdimage',
    'bootstrapform',
    'widget_tweaks',
    'admin_honeypot',
    'cookielaw', 

    # Local
    'core',
    'accounts',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOCKDOWN_PASSWORDS = ['hejsan123']

AUTH_USER_MODEL = 'accounts.CustomUser'

if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['0.0.0.0', '10.0.2.2']


MIDDLEWARE = [
    'allow_cidr.middleware.AllowCIDRMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Third party
    #"debug_toolbar.middleware.DebugToolbarMiddleware",
    # 'lockdown.middleware.LockdownMiddleware',

]

ROOT_URLCONF = 'kontorshund.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_admin_env_notice.context_processors.from_settings',
                'cookielaw.context_processors.cookielaw'
            ],
        },
    },
]

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

# Set color stripe in Django-Admin to production by default, otherwise to development
env_color = "#FF2222"
env_text_color = "#FFFFFF"

if (os.environ.get('IS_DEVELOPMENT')) == "TRUE":
    env_color = "#00FF00"
    env_text_color = "#000000"

ENVIRONMENT_NAME = os.environ.get("ENVIRONMENT_NAME") 
ENVIRONMENT_COLOR = env_color 
ENVIRONMENT_FLOAT = True
ENVIRONMENT_TEXT_COLOR = env_text_color


WSGI_APPLICATION = 'kontorshund.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get("DB_HOST"), 
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'PORT': os.environ.get("DB_PORT")
    }
}

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))


if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    print('TEST DB SETTINGS')
    DATABASES['default']['HOST'] = 'test-db'
    DATABASES['default']['NAME'] = 'postgres'
    DATABASES['default']['USER'] = 'postgres'
    DATABASES['default']['PASSWORD'] = 'postgres'
    DATABASES['default']['PORT'] = '5432'


    #DATABASES['default']['TEST_NAME'] = os.path.join(os.path.dirname(__file__), 'test.db'),



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'sv'

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

USE_S3 = os.environ.get("USE_S3", "false").lower() == "true"


if USE_S3:

    print("Using S3")

    # Linode bucket credentials
    LINODE_BUCKET_NAME=os.environ.get('LINODE_BUCKET_NAME')
    LINODE_BUCKET_REGION=os.environ.get('LINODE_BUCKET_REGION')
    LINODE_BUCKET_ACCESS_KEY=os.environ.get('LINODE_BUCKET_ACCESS_KEY') 
    LINODE_BUCKET_SECRET_KEY=os.environ.get('LINODE_BUCKET_SECRET_KEY') 

    # Static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{LINODE_BUCKET_NAME}.{LINODE_BUCKET_REGION}.linodeobjects.com/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'kontorshund.storage_backends.StaticStorage' # Add files to bucket when running collectstatic
    
    # Media settings
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{LINODE_BUCKET_NAME}.{LINODE_BUCKET_REGION}.linodeobjects.com/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'kontorshund.storage_backends.PublicMediaStorage'

    # Using AWS template settings for Boto3 with Linode crentials
    AWS_S3_ENDPOINT_URL=f'https://{LINODE_BUCKET_REGION}.linodeobjects.com'
    AWS_ACCESS_KEY_ID=LINODE_BUCKET_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY=LINODE_BUCKET_SECRET_KEY  
    AWS_S3_REGION_NAME=LINODE_BUCKET_REGION
    AWS_S3_USE_SSL=True
    AWS_STORAGE_BUCKET_NAME=LINODE_BUCKET_NAME
    AWS_DEFAULT_ACL= None


if not USE_S3:
    print("Not using S3")

    STATIC_URL = '/static/'
    STATIC_ROOT = '/home/dockeruser/web/staticfiles'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / "mediafiles"

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    print('Using test password hashing')
    # much faster password hashing, default one is super slow (on purpose)
    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']


# Where to collect static files from locally
STATICFILES_DIRS = [BASE_DIR / 'local_static']


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauth config

ACCOUNT_FORMS = {
    'login': 'core.forms.allauth_forms.CoreLoginForm',
    #'signup': 'core.forms.allauth_forms.CoreSignupForm',
    
    }


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Facebook
SOCIAL_AUTH_FACEBOOK_KEY = '596768574908566'  # App KEY
SOCIAL_AUTH_FACEBOOK_SECRET ='693a7cd09ba4ddadf46bdeadd3777f5f' #app secret

SITE_ID = 1

ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
LOGIN_REDIRECT_URL = 'list_postings'
ACCOUNT_LOGOUT_REDIRECT = 'list_postings'

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True  # False by default
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True  # True by default

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'


# EMAIL SETTINGS

# Use console-email if only using development server
if (os.environ.get('IS_DEVELOPMENT')) == "TRUE":
    print('Using email console backend')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


if (os.environ.get('IS_DEVELOPMENT')) == 'FALSE':

    print('Using live email settings')

    # Email settings
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.environ.get('EMAIL_SERVER_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_SERVER_PORT')
    EMAIL_HOST_USER = os.environ.get('EMAIL_SERVER_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_SERVER_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
    SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    print('Using secure SSL settings')
    # SECURE_SSL_REDIRECT = True
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    # SECURE_HSTS_SECONDS = 3600
    # SECURE_HSTS_PRELOAD = True
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # Sentry
    sentry_sdk.init(
    environment="production",
    dsn="https://4e72c8deb9024ec78e9ebe14d879b3fb@o1136966.ingest.sentry.io/6189092",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
    )



# LOGGING

ADMINS = (
    ('Alexander Lindgren', 'alexlindgren08@gmail.se'),
)

# Docker/Supervisord logging settings
LOGGING = DEFAULT_LOGGING
LOGGING['handlers']['console']['filters'] = ['require_debug_false']
LOGGING['loggers']['django.server']['propagate'] = True

if DEBUG == True:
    log_level = 'DEBUG'
else:
    log_level = 'INFO'

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored_verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(asctime)s %(log_color)s%(levelname)s   %(red)s%(module)s   %(yellow)s%(message)s   %(blue)s%(name)s.%(funcName)s:%(lineno)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'colored_console': {
            'level': log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'colored_verbose'
        },
         'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['colored_console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'gunicorn.access': {
            'handlers': ['colored_console']
        },
        'gunicorn.error': {
            'handlers': ['colored_console']
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # }
    }
}