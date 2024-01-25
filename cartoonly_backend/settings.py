import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3tf7jjjbqpb7dvwoz36ru6qj--m-6waardrf&k@$f-zbr@ouhs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.vercel.app', "*"]

AUTH_USER_MODEL = 'account.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    "corsheaders",
    'drf_yasg',

    'drf_spectacular',
    'drf_spectacular_sidecar',

    'account',
    'api',
    'admin_user',
    'portrait',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'user-agent',
    'x-csrftoken',
    'api-key',
    'Access-Control-Allow-Origin',
    'organisation',
]


ROOT_URLCONF = 'cartoonly_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cartoonly_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },

    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default="postgres://default:AXYDJxCcI4s8@ep-falling-violet-74277946.us-east-1.postgres.vercel-storage.com:5432/verceldb"
        )
    }



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db_prod.sqlite3',
#     },

# }
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.path.join('DATABASE_NAME'),
#         'USER': os.path.join('DATABASE_USERNAME'),
#         'PASSWORD': os.path.join('DATABASE_PASSWORD'),
#         'HOST': os.path.join('DATABASE_HOST'),
#         'PORT': os.path.join('DATABASE_PORT'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'https://hostel-staticfiles.vercel.app/static/cartonly/'
MEDIA_URL = 'https://hostel-staticfiles.vercel.app/media/cartonly/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static') ]  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SPECTACULAR_SETTINGS = {
    'TITLE': 'RADAR BACKEND',
    'DESCRIPTION': 'Radar service api documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayRequestDuration": True,
    },
}



GOOGLE_OAUTH2_CLIENT_ID=os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET=os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
BASE_FRONTEND_URL = os.environ.get('DJANGO_BASE_FRONTEND_URL', default='http://localhost:5173')



STRIPE_SECRET_KEY = 'sk_test_51OKGHRI65ur4oCTjhLVHtBAts6V0VwnAMZrcljpmFirpqGuGnT4eW6sBKTIQ2pzQQ31MaBjDeO67HwuiwtKI3B7R00oHlYWjWu'
# STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
# # This is your Stripe CLI webhook secret for testing your endpoint locally.
# STRIPE_WEBHOOK_SECRET=os.environ.get('STRIPE_WEBHOOK_SECRET')


REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY" : 'errors',
    "DEFAULT_AUTHENTICATION_CLASSES" : (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 5 
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS':{
        'Bearer':{
            'type':'apiKey',
            'name':'Authorization',
            'in':'header'
        }
    }
}



EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER="programmerolakay@gmail.com"
EMAIL_HOST_PASSWORD="xsivhbybtzhuwvul"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'