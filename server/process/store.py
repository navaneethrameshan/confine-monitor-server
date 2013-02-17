
from couchdb import *

def get_db(name = 'test'):
    s = Server("http://127.0.0.1:5984/")
    if not s.__contains__(name):
        db = s.create(name)
    else:
       db = s.__getitem__(name)

    return db


def store_document(doc_id, values, db):
    db[doc_id] = values
    print db[doc_id].items()

def update_document(doc_id, values,db):
    if doc_id in db:
        print ("Updating reference document")
        document = db[doc_id]
        values['_rev'] = document['_rev']
        db[doc_id] = values
    else:
        print ("Creating reference document")
        store_document(doc_id, values, db)