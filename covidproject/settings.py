"""This is a control file for settings. Determines whether app is being used
in production or for local testing by searching for a 'local_settings.py' file.
"""

import os

from .base_settings import *


if os.path.isfile(os.path.join(BASE_DIR, 'covidproject/local_settings.py')):
    # Running locally.
    from .local_settings import *
else:
    # Production
    from .production_settings import *

    from django_heroku import settings
    # Let heroku set values.
    settings(globals())
