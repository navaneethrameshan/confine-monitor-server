import os
import pickle
import shelve
import logging
from couchbase.client import Couchbase
from server import constants
from server.couchbase import util
from server.logger import logger

log = logger("store")

class Database(object):

    def __init__(self, name = 'check'):
        cb = Couchbase(util.DB_IP+":"+util.DB_PORT, "Administrator", "couchbase")
        self.log = logger ("database")

        try:
            bucket = cb.create(name, ram_quota_mb=100, replica=1)
        except:
            bucket = cb[name]

        self.bucket = bucket


    def store_document(self, doc_id, values):
        self.log.debug("Storing Document with DocID: %s" %doc_id)
        self.bucket[doc_id] = values


    def update_document(self, doc_id, values):
        self.log.debug("Updating reference document: %s" %doc_id)
        #document = db[doc_id]
        #values['_rev'] = document['_rev']
        self.store_document(doc_id, values)

    def get_bucket(self):
        self.log.debug("Getting bucket: " + str(self.bucket))
        return self.bucket


def create_database():
    log.debug("Attempting to create Database instance")
    constants.database_list.append(Database())


def get_bucket():
    log.debug("Attempting to fetch bucket")
    return constants.database_list[0].get_bucket()


def store_document( doc_id, values):
    log.debug("Attempting to store document")
    constants.database_list[0].store_document(doc_id, values)

def update_document( doc_id, values):
    log.debug("Attempting to update document")
    constants.database_list[0].update_document(doc_id,values)

