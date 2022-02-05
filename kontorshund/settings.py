import os
from pathlib import Path
from urllib.parse import urljoin
from django.utils.log import DEFAULT_LOGGING
from django.contrib.messages import constants as messages



# Price constants
PRICE_SWISH_INITIAL = '1 kr'
PRICE_SWISH_INITIAL_IN_SEK = 1
PRICE_SWISH_EXTEND = '2 kr'
PRICE_SWISH_EXTEND_IN_SEK = 2
PRICE_BANKGIRO_INITIAL = '1 kr'


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
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", " ").split(" ")
ALLOWED_HOSTS.append(ALLOWED_NGROK)

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
    'silk',
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

    # Local
    'core',
    'accounts',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOCKDOWN_PASSWORDS = ['sP4%tF_"QPHn4Z@k']

# LOCKDOWN_URL_EXCEPTIONS = (
#     r'^/generate-swish-qr-code/$',   # unlock /about
#     r'^/generate-swish-request-token/$',   # unlock /about
#     r'^/generate-swish-qr-code/$',   # unlock /about
#     r'^/check-payment-status/[0-9]*$',   # unlock /about
#     r'^/swish-successfull-android$',   # unlock /about
#     r'^/ajax/load-municipalities/$',   # unlock /about
#     r'^/ajax/load-areas/$',   # unlock /about
#     r'^/breed-autocomplete$',   # unlock /about
# )


CISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'accounts.CustomUser'

if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['0.0.0.0', '10.0.2.2']


MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    
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

if (os.environ.get('IS_DEVELOPMENT')) == "True":
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
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"), 
        'PORT': os.environ.get("DB_PORT")
    }
}



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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

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
    STATIC_URL = f'https://{LINODE_BUCKET_NAME}.{LINODE_BUCKET_REGION}.linodeobjects.com/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'kontorshund.storage_backends.PublicMediaStorage'

    # Using AWS template settings for Boto3 with Linode crentials
    AWS_S3_ENDPOINT_URL=f'https://{LINODE_BUCKET_REGION}.linodeobjects.com'
    AWS_ACCESS_KEY_ID=LINODE_BUCKET_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY=LINODE_BUCKET_SECRET_KEY
    AWS_S3_REGION_NAME=LINODE_BUCKET_REGION
    AWS_S3_USE_SSL=True
    AWS_STORAGE_BUCKET_NAME=LINODE_BUCKET_NAME
    AWS_DEFAULT_ACL= None

else:
    print("Not using S3")

    STATIC_URL = '/static/'
    STATIC_ROOT = '/home/kontorshund/web/staticfiles'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / "mediafiles"


# Where to collect static files from locally
STATICFILES_DIRS = [BASE_DIR / 'local_static']


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauth config

ACCOUNT_FORMS = {
    'login': 'core.forms.allauth_forms.CoreLoginForm',
    'signup': 'core.forms.allauth_forms.CoreSignupForm',
    
    }


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {

    # Facebook
    # 'facebook': {
    #     'METHOD': 'oauth2',
    #     'SCOPE': ['email','public_profile', 'user_friends'],
    #     'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    #     'FIELDS': [
    #         'id',
    #         'email',
    #         'name',
    #         'first_name',
    #         'last_name',
    #         'verified',
    #         'locale',
    #         'timezone',
    #         'link',
    #         'gender',
    #         'updated_time'],
    #     'EXCHANGE_TOKEN': True,
    #     'LOCALE_FUNC': lambda request: 'kr_KR',
    #     'VERIFIED_EMAIL': False,
    #     'VERSION': 'v2.4'
    # },

    # Google
    # 'google': {
    #     'SCOPE': [
    #         'profile',
    #         'email',
    #     ],
    #     'AUTH_PARAMS': {
    #         'access_type': 'online',
    #     }
    # }
}

# Facebook
SOCIAL_AUTH_FACEBOOK_KEY = '596768574908566'  # App KEY
SOCIAL_AUTH_FACEBOOK_SECRET ='693a7cd09ba4ddadf46bdeadd3777f5f' #app secret

SITE_ID = 1

ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
LOGIN_REDIRECT_URL = 'index'
ACCOUNT_LOGOUT_REDIRECT = 'index'

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True  # False by default
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True  # True by default

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'


# EMAIL SETTINGS

# Use console-email if only using development server
if (os.environ.get('IS_DEVELOPMENT')) == "True":
    print('is development = True')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


if (os.environ.get('IS_DEVELOPMENT')) == 'False':

    print('Using live email settings')

    # Email settings
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'mailcluster.loopia.se'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'info@kontorshund.se'
    EMAIL_HOST_PASSWORD = 'W3;qU]8;-:Pk4`}q`G8&<m=-X2&/E'
    DEFAULT_FROM_EMAIL = 'Kontorshund.se <info@kontorshund.se>'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# LOGGING

ADMINS = (
    ('Alexander Lindgren', 'alexlindgren08@gmail.se'),
)

# Docker/Supervisord logging settings
LOGGING = DEFAULT_LOGGING
LOGGING['handlers']['console']['filters'] = ['require_debug_false']
LOGGING['loggers']['django.server']['propagate'] = True

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
        }
    },
    'handlers': {
        'colored_console': {
            'level': 'INFO',
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
            'level': 'INFO',
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
        }
    }
}