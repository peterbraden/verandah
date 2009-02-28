DEBUG = True
TEMPLATE_DEBUG = DEBUG
CONFIG = "dev"

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
ADMIN_MEDIA_PREFIX = '/adminmedia/'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'verandah.urls'
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'cal.context.glob',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.webdesign',
    'cal',
    'typewriter'
)
