#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
import os
from environment.base import set_environment
from environment.variables import EnvironmentVariable


def main():
    set_environment('MAIN')
    try:
        from django.core.management.commands.runserver import Command as runserver
        runserver.default_port = os.environ.get('PORT', 8000)
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
