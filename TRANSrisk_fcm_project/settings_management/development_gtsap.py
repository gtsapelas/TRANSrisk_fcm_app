from TRANSrisk_fcm_project.settings_management.development import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'transrisk_fcm_db',
        'USER': 'postgres',
        'PASSWORD': 'sssshmmy',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'

#Oi 2 grammes apo kato prostethikan giati allios evgaze minima lathous sto signup, eno ekane kanonika to signup. I proti grammi xreiazetai sigoura
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'