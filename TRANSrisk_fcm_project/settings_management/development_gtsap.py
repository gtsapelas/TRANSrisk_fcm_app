from TRANSrisk_fcm_project.settings_management.development import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'transrisk_fcm_db',
        'USER': 'Giannis',
        'PASSWORD': '13131313',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
