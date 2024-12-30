from pathlib import Path
import os
import re
import dj_database_url
from corsheaders.defaults import default_headers
from datetime import timedelta

# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# ----------------------------------------------------------------#
# HOT TO SET UP CORS:
# https://github.com/adamchainz/django-cors-headers#configuration
# ----------------------------------------------------------------#


if os.path.exists('env.py'):
    import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG is False - the authentication token will be stored in cookies
# rather than being passed in the Authorization header.

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': CLOUDINARY_URL
}
MEDIA_URL = '/media/'  # or any prefix you choose
MEDIA_URL = os.environ.get('MEDIA_URL')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
        if DEBUG
        else 'rest_framework_simplejwt.authentication.JWTAuthentication'
        # else 'dj_rest_auth.jwt_auth.JWTAuthentication'
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DATETIME_FORMAT': '%d %b %Y',
}

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]

# JWT configuration
SIMPLE_JWT = {
    'ALGORITHM': 'HS256',  # Common choice
    'AUTH_COOKIE': 'jwt-auth',
    'AUTH_COOKIE_SECURE': not DEBUG,  # for local dev False, True for production
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'Lax',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # Update last_login field on token issue
}

if not DEBUG:
    REST_USE_JWT = True

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG  # False for local dev, True for production

CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = False  # Must be False for frontend access
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG  # False for local dev, True for production


# PRODUCTION SETTINGS
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# JWT_AUTH_SECURE = False if DEBUG else True
# JWT_AUTH_COOKIE = 'my-app-auth'
# JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
# JWT_AUTH_SAMESITE = 'None'

REST_AUTH = {
    'USER_DETAILS_SERIALIZER': 'drf_api.serializers.CurrentUserSerializer'
}

LOGIN_REDIRECT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-$pee69*^#acm@1altks^&^!n1p^=oh%yj=1%xpxji(pph7tpxj'
SECRET_KEY = os.getenv('SECRET_KEY')

# To use the API with React app: ALLOWED_HOST and CLIENT_ORIGIN_DEV in heroku
ALLOWED_HOSTS = [
    "8000-eneliviu-djrestapi-vo4ia7gx81e.ws.codeinstitute-ide.net",
    '3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net',
    '127.0.0.1',
    'localhost',
    'dj-drf-api-763634fa56e5.herokuapp.com'
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
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    # Own applications
    'profiles',
    'posts',
    'comments',
    'likes',
    'followers',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# if 'CLIENT_ORIGIN' in os.environ:  # For Heroku deployment only
# The API will use the CLIENT_ORIGIN variable, which is the front end app's url.
# If the variable is not present, the project is still in development, so then
# the regular expression in the else statement will allow requests that are coming from your IDE.

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    'https://react-dj-restapi-eb6a7149ec97.herokuapp.com',
    'https://3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net',
    'https://react-frontend-api-b166a083b609.herokuapp.com',
    'https://dj-drf-api-763634fa56e5.herokuapp.com'
]
client_origin = os.environ.get('CLIENT_ORIGIN')
if client_origin:
    CORS_ALLOWED_ORIGINS.append(client_origin)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    'https://8000-eneliviu-djrestapi-vo4ia7gx81e.ws.codeinstitute-ide.net',
    'https://3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net',
    'https://react-frontend-api-b166a083b609.herokuapp.com/signup',
    'https://dj-drf-api-763634fa56e5.herokuapp.com'
]


# else:
#     CORS_ALLOWED_ORIGIN_REGEXES = [
#         # r"^https:\/\/.*\.codeinstitute-ide\.net$"
#         r"^https://\w+\.codeinstitute-ide\.net$",
#     ]

# Allow All Origins for Debug:
# CORS_ALLOWED_ORIGINS = [
#     'https://react-frontend-api-b166a083b609.herokuapp.com',
# ]

# CORS_ORIGIN_WHITELIST = (
#     "https://8000-eneliviu-djrestapi-vo4ia7gx81e.ws.codeinstitute-ide.net",
#     "https://3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net"
# )

# if 'CLIENT_ORIGIN_DEV' in os.environ:
#     extracted_url = re.match(
#         r'^.+-', os.environ.get('CLIENT_ORIGIN_DEV', ''), re.IGNORECASE
#     ).group(0)
#     CORS_ALLOWED_ORIGIN_REGEXES = [
#         # rf"{extracted_url}(eu|us)\d+\w\.codeinstitute-ide\.net$",
#         r"^https:\/\/.*\.codeinstitute-ide\.net$",
#     ]

# For Heroku deployment:
# if 'CLIENT_ORIGIN_DEV' in os.environ:
#     CORS_ALLOWED_ORIGIN_REGEXES = [
#         r"^https:\/\/.*\.codeinstitute-ide\.net$",
#     ]


# JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
# JWT_AUTH_SAMESITE = 'None'  # Frontend and the API on different platforms


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

# Database Configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3' if DEBUG else 'django.db.backends.postgresql',
#         'NAME': BASE_DIR / 'db.sqlite3' if DEBUG else dj_database_url.config(os.getenv('DATABASE_URL'))
#     }
# }

# DATABASES = {
#     'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set the maximum file upload size to 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB in bytes

# Set the maximum request body size to 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB in bytes

# Define a custom maximum upload size for use in validation
MAX_UPLOAD_SIZE = 10485760  # 10 MB in bytes
