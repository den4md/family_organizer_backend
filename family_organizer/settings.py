from pathlib import Path

# Base settings

BASE_DIR = Path(__file__).resolve().parent.parent

# noinspection SpellCheckingInspection
SECRET_KEY = '8)3y%w6alvr*=thf(ws3w34^+z*k&_jzn(rs7k3t+$cks1ltu8'

DEBUG = True

ALLOWED_HOSTS = [
    '94.243.97.68',  # For dynamic IP this need to be changed
    '192.168.1.20',
    '127.0.0.1',
    '0.0.0.0',
]


# User-defined settings

AUTH_USER_MODEL = 'api.User'
INVITE_INTENT = 'app://family-organizer.com/'
FILE_STORAGE = 'files/'
TEMP_STORAGE = 'tmp/'
IMAGE_MIN_SIZE = 300  # px
IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'ico', 'webp']


# Application definition

INSTALLED_APPS = [
    'api.apps.ApiConfig',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'family_organizer.urls'

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

WSGI_APPLICATION = 'family_organizer.wsgi.application'


# Database

# noinspection SpellCheckingInspection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'family_organizer_db',
        'USER': 'api_app',
        'PASSWORD': 'api_apppassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
