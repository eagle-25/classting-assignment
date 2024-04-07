from common.settings import *  # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
    'replica': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {
            'MIRROR': 'default',
        },
    },
}
