from TRANSrisk_fcm_project.settings_management.base_settings import *

import dj_database_url

# Update database configuration with $DATABASE_URL.
DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = ["*"]
DEBUG = False
