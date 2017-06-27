from TRANSrisk_fcm_project.settings_management.base_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'transrisk_fcm_db',
    }
}

# No emails should be sent on development
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
CONTACT_EMAIL = 'myemail@gmail.com'
