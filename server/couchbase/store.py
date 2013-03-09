import os
import pickle
import shelve
from couchbase.client import Couchbase
from server import constants

class Database(object):

    def __init__(self, name = 'test'):
        cb = Couchbase("147.83.35.241:8091", "Administrator", "couchbase")

        try:
            bucket = cb.create(name, ram_quota_mb=100, replica=1)
        except:
            bucket = cb[name]

        self.bucket = bucket


    def store_document(self, doc_id, values):
        self.bucket[doc_id] = values


    def update_document(self, doc_id, values):
        print ("Updating reference document")
        #document = db[doc_id]
        #values['_rev'] = document['_rev']
        self.store_document(doc_id, values)

    def get_bucket(self):
        return self.bucket


def create_database():
    constants.database_list.append(Database())


def get_bucket():
    return constants.database_list[0].get_bucket()


def store_document( doc_id, values):
    constants.database_list[0].store_document(doc_id, values)

def update_document( doc_id, values):
    constants.database_list[0].update_document(doc_id,values)

