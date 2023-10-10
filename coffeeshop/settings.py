"""
Django settings for coffeeshop project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


import os
from pathlib import Path

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv
load_dotenv()          # take environment variables from .env.       



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY'),

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ '127.0.0.1', 'localhost']

                   



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My local apps
    'users.apps.UsersConfig',
    'pages.apps.PagesConfig',
    'products.apps.ProductsConfig',
    'ecommerce.apps.EcommerceConfig',
    # Third party apps
    
    # https://django-phonenumber-field.readthedocs.io/en/latest/
    "phonenumber_field",
    # https://pypi.org/project/django-crispy-forms/
    "crispy_forms",
    # https://pypi.org/project/crispy-bootstrap4/
    "crispy_bootstrap4",
    # https://fontawesome.com/docs/web/use-with/python-django
    "fontawesomefree",

    # https://django-bootstrap-datepicker-plus.readthedocs.io/en/latest/Getting_Started.html#install
    ############# django-bootstrap-datepicker-plus ###
    # https://monim67.github.io/django-bootstrap-datepicker-plus/configure/

     ############# django-bootstrap-datepicker-plus ###
    # https://monim67.github.io/django-bootstrap-datepicker-plus/configure/

    # https://pypi.org/project/django-bootstrap-datepicker-plus/
    "bootstrap_datepicker_plus",

    # https://pypi.org/project/django-bootstrap4/
    "bootstrap4",

    # https://pypi.org/project/django-countries/
    "django_countries",

    # https://pypi.org/project/django-forms-bootstrap/
    'django_forms_bootstrap',

    # https://pypi.org/project/django-widget-tweaks/
    'widget_tweaks',

    # https://django-hitcount.readthedocs.io/en/latest/installation.html
    "hitcount",
]






MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coffeeshop.urls'

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
                 # Our context processor:
                "ecommerce.context_processors.cart_quant",
            ],
        },
    },
]

WSGI_APPLICATION = 'coffeeshop.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    # Development
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': os.getenv('DB_NAME'),

        'USER': os.getenv('DB_USER'),

        'PASSWORD': os.getenv('DB_PASSWORD'),

        'HOST': os.getenv('DB_HOST'),

        'PORT': os.getenv('DB_PORT'),
    }
   
    #PRODUCTION
    # 'default': dj_database_url.config(
    #     default=os.getenv('DATABASE_URL'), 
    #     conn_max_age=600    
    #     )
}
#print(DATABASES)


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
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
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')       

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




############################################# custom user model settings ##############################################
# AUTH_USER_MODEL = "myapp.MyUser"
# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
AUTH_USER_MODEL = 'users.UserModel'




############################################# EMAIL settings ##############################################
# At this stage, we are going to configure email backend to send confirmation links. Let's test it on console for this tutorial.
EMAIL_BACKEND      = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@CoffeeShop'





#################################### django-rest-passwordreset settings ##############################################
# Time in hours about how long the token is active
DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 6

# Return 200 even if the user doesn't exist in the database
DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = True

# Allow password reset for a user that does not have a usable password
DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD = True




####################################### CRISPY FORM ##############################################
# https://pypi.org/project/crispy-bootstrap4/
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"



####################################### STRIPE_SECRET SETTINGS ##############################################
# https://dashboard.stripe.com/test/apikeys

STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')


