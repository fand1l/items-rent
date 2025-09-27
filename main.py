# Server starter

import os
import sys
import django
from django.core.management import execute_from_command_line

IP = "0.0.0.0"
PORT = "8000"
DEBUG = True

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ItemsRent.settings")
    django.setup()
    execute_from_command_line([sys.argv[0], "runserver", f"{IP}:{PORT}"])