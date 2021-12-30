import os
from pathlib import Path
from urllib.parse import urljoin

# Price constants
PRICE_SWISH = '1 kr'
PRICE_SWISH_IN_SEK = 1
PRICE_BANKGIRO = '1 kr'

# Swish constants
NGROK_URL = "https://ca31-92-33-202-136.ngrok.io" # Fill out with new value when testing 
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

    # Local
    'accounts',
    'core',
]

LOCKDOWN_PASSWORDS = ['sP4%tF_"QPHn4Z@k']

LOCKDOWN_URL_EXCEPTIONS = (
    r'^/generate-swish-qr-code/$',   # unlock /about
    r'^/generate-swish-request-token/$',   # unlock /about
    r'^/generate-swish-qr-code/$',   # unlock /about
    r'^/check-payment-status/$',   # unlock /about
    r'^/swish-successfull-android$',   # unlock /about
    r'^/ajax/load-municipalities/$',   # unlock /about
    r'^/ajax/load-areas/$',   # unlock /about
    r'^/breed-autocomplete$',   # unlock /about


)


CISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'accounts.CustomUser'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lockdown.middleware.LockdownMiddleware',

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

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "mediafiles"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauth config


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

# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'mailcluster.loopia.se'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@kontorshund.se'
EMAIL_HOST_PASSWORD = 'W3;qU]8;-:Pk4`}q`G8&<m=-X2&/E'
DEFAULT_FROM_EMAIL = 'Kontorshund.se <info@kontorshund.se>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Use console-email if only using development server
if (os.environ.get('IS_DEVELOPMENT')) == "True":
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



