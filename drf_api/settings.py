"""
Django settings for drf_api project.

Generated by 'django-admin startproject' using Django 3.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import re
import dj_database_url


# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# ----------------------------------------------------------------#
# HOT TO SET UP CORS:
# https://github.com/adamchainz/django-cors-headers#configuration
# ----------------------------------------------------------------#


if os.path.exists('env.py'):
    import env

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = 'DEV' in os.environ  # Bool

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}
MEDIA_URL = '/media/'  # or any prefix you choose
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [(
        'rest_framework.authentication.SessionAuthentication'
        if 'DEV' in os.environ
        else [
                'rest_framework.authentication.TokenAuthentication',
                'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
            ]
        
    )],
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DATETIME_FORMAT': '%d %b %Y',  # day, month abbrev, year 4 digits
}

# if 'DEV' not in os.environ:
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ]



REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'jwt-access-token'  # 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
JWT_AUTH_SAMESITE = 'None'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'drf_api.serializers.CurrentUserSerializer'
}

LOGIN_REDIRECT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-$pee69*^#acm@1altks^&^!n1p^=oh%yj=1%xpxji(pph7tpxj'
SECRET_KEY = os.getenv('SECRET_KEY')

# To use the API with React app, add environment variables: ALLOWED_HOST and CLIENT_ORIGIN_DEV in heroku
ALLOWED_HOSTS = [
    '8000-eneliviu-djrestapi-vo4ia7gx81e.ws.codeinstitute-ide.net',
    'https://react-dj-restapi-eb6a7149ec97.herokuapp.com',
    'https://3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net',
    '.herokuapp.com',
    'https://*.herokuapp.com',
    'https://*.127.0.0.1',
    'localhost',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',

    'profiles',
    'posts',
    'comments',
    'likes',
    'followers',
]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

if 'CLIENT_ORIGIN' in os.environ:
    # The API will use the CLIENT_ORIGIN variable, which is the front end app's url.
    # If the variable is not present, the project is still in development, so then
    # the regular expression in the else statement will allow requests that are coming from your IDE.
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CLIENT_ORIGIN'),
        # 'https://*.127.0.0.1',
        # 'https://react-dj-restapi-eb6a7149ec97.herokuapp.com',
        # 'https://3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net',
        ]
else:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https:\/\/.*\.codeinstitute-ide\.net$",
    ]

# if 'CLIENT_ORIGIN_DEV' in os.environ:
#     extracted_url = re.match(
#         r'^.+-', os.environ.get('CLIENT_ORIGIN_DEV', ''), re.IGNORECASE
#     ).group(0)
#     CORS_ALLOWED_ORIGIN_REGEXES = [
#         # rf"{extracted_url}(eu|us)\d+\w\.codeinstitute-ide\.net$",
#         r"^https:\/\/.*\.codeinstitute-ide\.net$",
#     ]

if 'CLIENT_ORIGIN_DEV' in os.environ:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https:\/\/.*\.codeinstitute-ide\.net$",
    ]

CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = False


JWT_AUTH_REFRESH_COOKE = 'my-refresh-token'
JWT_AUTH_SAMESITE = 'None'  # Frontend and the API on different platforms

ROOT_URLCONF = 'drf_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'drf_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': ({
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    } if 'DEV' in os.environ else dj_database_url.parse(
        os.environ.get('DATABASE_URL')
    ))
}

CSRF_TRUSTED_ORIGINS = [
    "https://*.codeinstitute-ide.net",
    "https://*.herokuapp.com",
    'https://*.127.0.0.1',
    "https://8000-eneliviu-djrestapi-vo4ia7gx81e.ws.codeinstitute-ide.net",
]

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
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
