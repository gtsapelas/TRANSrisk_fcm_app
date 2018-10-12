from TRANSrisk_fcm_project.settings_management.base_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ddbso8btmk2j1i',
        'USER': 'mxuhuoymiyjacp',
        'PASSWORD': '1daacb5325597a7465bbd7a74cca1b0f175e73fc7da2f83d44a50e77a3a056de',
        'HOST': 'ec2-54-227-251-233.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

