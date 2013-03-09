#!/usr/bin/env python
import os
import sys

from server.couchbase import store

def get_database_object():
   db = store.create_database()


if __name__ == "__main__":

    get_database_object()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
