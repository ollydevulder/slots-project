#       ==Settings for Slots App==
#       Determines if project is being run locally
#       or in production. It does this by checking
#       for a .env file in the root dir.
#       Therefore, when running locally, a .env
#       file is required as well as a
#       localsettings.py file. (in this directory)


import os

from .base_settings import *

# Purposefully duplicated. (Sorry DRY)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.path.isfile(os.path.join(BASE_DIR, '.env')):
    # Running locally.
    from .local_settings import *
else:
    # Production
    from .production_settings import *
