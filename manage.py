#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from py2neo import neo4j
from py2neo import node, rel
from mmamathapi.modules.models import Fighter

def initialize_neo4j_database():
  db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmamathapi.settings')
    try:
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
