#!/usr/bin/env python
import os
import sys
from common import nodelist
from server import constants

from server.couchbase import store

def get_database_object():
   db = store.create_database()


def cache_nodes_list():
    constants.nodes = nodelist.get_node_list()

if __name__ == "__main__":

    get_database_object()

    cache_nodes_list()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
