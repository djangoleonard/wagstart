from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '6xz8ajb2pwe%@%+xka)id&w4h7qe^999%+_or^(-^@)zm6spi-'
#
#
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
