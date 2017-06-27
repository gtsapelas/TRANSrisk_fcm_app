import os

# import the appropriate settings file
if os.environ.get('Production', '') == 'On':
    # production settings
    from TRANSrisk_fcm_project.settings_management.production import *
else:
    try:
        # custom settings files
        settings_files = [sf.strip() for sf in
                          open('TRANSrisk_fcm_project//settings_management/settings-loader.txt', 'r').read().split(',')]

        for settings_file in settings_files:
            if settings_file == 'development_gtsap':
                from TRANSrisk_fcm_project.settings_management.development_gtsap import *
            elif settings_file == 'development':
                from TRANSrisk_fcm_project.settings_management.development import *
    except IOError:
        # default development settings
        from TRANSrisk_fcm_project.settings_management.development import *
