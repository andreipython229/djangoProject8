#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # путь до корня проекта
sys.path.insert(0, BASE_DIR)                            # добавляем корень проекта
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))   # добавляем backend

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject8.settings")
    # теперь settings будет искаться в backend/djangoProject8/settings.py
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
