#!/usr/bin/env python3

"""A tool for setting up local testing env."""

import os
import sys
import subprocess

try:
    from django.core.management import execute_from_command_line as ex
except ImportError:
    print('Django not found.')
    print('Attempting install...')
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', 'django'])
    except:
        print('Couldn\'t install django. Is pip version current?')
        exit()
    from django.core.management import execute_from_command_line as ex


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covidproject.settings')
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'covidproject')

# Check for local_settings.py

file_path = os.path.join(DIR, 'local_settings.py')

if not os.path.isfile(file_path):
    # File doesn't exist.
    # Create it.
    print(f'{file_path} not found.')
    print('Creating...', end='')

    with open(file_path, 'w') as f:
        f.write('# Auto-generated by local_setup.py\n\nDEBUG = True')

    print('done!')
else:
    print(f'Found local settings.') 
    
# Migrations    

print('Attempting migrations...')
try:
    ex(('', 'makemigrations', 'slots'))
    ex(('', 'migrate'))
except:
    print('Couldn\'t make migrations, something went wrong.'
          '\nIs DJANGO_SETTINGS_MODULE set?')
    exit()

print('Finished setup.')
